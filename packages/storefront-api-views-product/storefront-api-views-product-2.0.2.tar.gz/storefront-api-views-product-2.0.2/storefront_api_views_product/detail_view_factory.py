from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Set

from storefront_product_adapter.facades import PricingFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition

from storefront_api_views_product.facades import BuyboxPreferenceFacade

from .errors import ViewConfigurationError
from .views.buybox import BuyboxDetailView, BuyboxDetailViewFactory

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import (
        ProductlineAdapter,
        VariantAdapter,
        OfferAdapter,
    )
    from storefront_product_adapter.collections import VariantCollection


from .views.enhanced_ecommerce import (
    EnhancedEcommerceAddToCartView,
    EnhancedEcommerceAddToCartViewFactory,
    EnhancedEcommerceClickView,
    EnhancedEcommerceClickViewFactory,
    EnhancedEcommerceImpressionView,
    EnhancedEcommerceImpressionViewFactory,
    EnhancedEcommerceListName,
)


class DetailViewFactory:
    """
    A convenience factory used to create any detail views for a given lineage.
    Mainly to be used by the PDP main endpoints, but also feeds. Any builders
    that are common with and produce the same content as the summary view factory
    will just call the summary view factory.
    """

    _buybox_type: BuyboxType
    _platform: Platform
    _pricing_facade: PricingFacade
    _selected_variant: Optional[VariantAdapter]
    _enabled_variants: VariantCollection  # Caller provided
    _buyable_variants: VariantCollection  # Internally filtered
    _non_buyable_variants: VariantCollection  # Internally filtered
    _winning_offers: Dict[BuyboxType, OfferAdapter]

    def __init__(
        self,
        *,
        platform: Platform,
        buybox_type: Optional[BuyboxType],
        productline: Optional[ProductlineAdapter] = None,
        enabled_variants: Optional[VariantCollection] = None,
    ) -> None:
        """
        Only one of the parameters `productline` and `variants` can be specified.

        If `enabled_variants` is given, this factory will use it as is. The idea is
        that if the caller applied other filtering (e.g. selectors) first, we don't
        ignore that. If a caller decided to pass disabled variants here, they should
        accept the effect it may or may not have.

        The parameter can change to have a default of None once OfferOpt is fully
        rolled out. This is similar to the SummaryViewFactory.

        Parameters
        ----------
        buybox_type:
            The buybox type to use.
            * With OfferOpt disabled, Cat V2 must set this to CUSTOM_1.
            * With OfferOpt enabled, this should never be CUSTOM_1 and the value will
              only be used when a single variant is selected (the given
              `variants` only contains one item or the given `productline` only has one
              buyable variant).

            The Product BFF must set this when a user has selected a variant and
            has chosen a preferred offer. When a variant is selected initially set
            this to None to use the default (which is a business rule).

            Set this to None to let the library pick the default, which will currently
            always be `lowest_priced`. This is allowed when there is a single variant
            selected as well.
        productline:
            If specified, enabled variants from this productline will be used. This
            is not expected to be used, but the option is here.
        enabled_variants:
            If specified, this collection and its productline will be used. Use this
            if any selector filtering was applied.
            An empty collection is allowed, but not all views will be buildable and
            may throw exceptions. For example, views that need pricing won't be able
            to get prices. Views that need productline level data will still try
            to access it via the collection's productline.


        enabled_variants:
            If specified, this collection and its productline will be used. Use this
            if any selector filtering was applied.
            An empty collection is allowed, but not all views will be buildable and
            may throw exceptions. For example, views that need pricing won't be able
            to get prices. Views that need productline level data will still try
            to access it via the collection's productline.
        """

        # First the important things. Without a productline or variants we can't do
        # anything useful.
        if enabled_variants is None and productline is not None:
            enabled_variants = CollectionsFactory.variants_from_productline_adapter(
                productline
            )
            self._enabled_variants = enabled_variants.filter_by_availability(
                (AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE)
            )
        elif productline is None and enabled_variants is not None:
            self._enabled_variants = enabled_variants
        else:
            raise ViewConfigurationError(
                "Either `productline` or `variants` must be given, exclusively."
            )

        self._selected_variant = self._enabled_variants.get_singular()

        # Make sure we pick the default offer/buybox preference if we don't have one
        # or shouldn't have one. If the caller gives a variant collection that has
        # only one item and that item is not buyable, we want the default.
        # We do not need the same custom_1 guarding here as in the summary-buybox
        # factory since this is only used by OfferOpt enabled code.
        if (
            not buybox_type
            or not self._selected_variant
            or not self._selected_variant.availability.is_buyable()
        ):
            buybox_type = BuyboxPreferenceFacade.get_default_for_variants(
                self._enabled_variants
            )

        self._platform = platform
        self._buybox_type = buybox_type
        self._buybox_type_displays = (
            BuyboxPreferenceFacade.get_display_preference_for_variants(
                self._enabled_variants
            )
        )
        self._winning_offers = {}

        # Some heavier lifting that still needs to happen is separated from the rest
        # of the constructor for readability
        self._hefty_init()

    def _hefty_init(self) -> None:
        pricing_collections = CollectionsFactory.pricing_from_variants(
            variants=self._enabled_variants,
            platform=self._platform,
            buybox_type=self._buybox_type,
            buybox_conditions_precedence=[
                OfferCondition.NEW,
                OfferCondition.USED,
            ],
        )
        self._buyable_variants = pricing_collections.buyable_variants
        self._non_buyable_variants = pricing_collections.non_buyable_variants

        self._pricing_facade = PricingFacade(collections=pricing_collections)

        self._pick_winners()

        # If there is only one winner, it would have won both buybox types. So
        # to keep things consistent, override the user selection (if any) with
        # the first buybox type that won. Since a user should not be able to select
        # something when there is only one winner, this should not happen unless
        # they edit the URL or have an old bookmark.
        if len(self._winning_offers) == 1:
            self._buybox_type = next(iter(self._winning_offers))

    def _pick_winners(self) -> None:
        """
        TODO: Decide if this is best suited in the product-adapter library
        as something like a BuyboxFacade.
        """
        if not self._selected_variant:
            return

        # First see if we have new offers winning. If not, fallback to used.
        offer_ids_seen: Set[int] = set()
        for display_buybox in self._buybox_type_displays:
            buybox_ids = self._selected_variant.get_buybox_offer_ids(
                platform=self._platform, buybox_type=display_buybox
            )
            offer_ids = buybox_ids.new
            if not offer_ids:
                continue

            # If an offer already won a buybox type, we don't want the same
            # winner to cause the second buybox type to display.
            offer_id = offer_ids[0]
            if offer_id in offer_ids_seen:
                continue
            offer = self._selected_variant.offers[offer_id]
            self._winning_offers[display_buybox] = offer
            offer_ids_seen.add(offer_id)

        # If we have NEW offers, we're done.
        if offer_ids_seen:
            return

        # For now, keep it simple and only use one buybox type for used offers.
        # It's unlikely, but possible, to have two different winners here, so
        # if we want to display both we change this to be similar to above.
        display_buybox = self._buybox_type_displays[0]
        buybox_ids = self._selected_variant.get_buybox_offer_ids(
            platform=self._platform, buybox_type=display_buybox
        )
        offer_ids = buybox_ids.used
        if not offer_ids:
            return

        offer_id = offer_ids[0]
        offer = self._selected_variant.offers[offer_id]
        self._winning_offers[display_buybox] = offer

    @property
    def winning_offers(self) -> Dict[BuyboxType, OfferAdapter]:
        """
        Arguably not meant to reside inside this factory, but the Product BFF will
        need to make sure it uses the same winners when building other views (like
        Other Offers) and this is the easiest way to keep it in sync right now.
        """
        return self._winning_offers

    def build_buybox(
        self,
        free_shipping_threshold: int,
        heavy_charge: Optional[float] = None,
    ) -> BuyboxDetailView:
        """
        heavy_charge:
            The extra delivery cost for a heavy item, if the item has the attribute
            that marks it as such.
        """
        factory = BuyboxDetailViewFactory(
            platform=self._platform,
            buybox_type=self._buybox_type,
            variants=self._enabled_variants,
            winning_offers=self._winning_offers,
            pricing=self._pricing_facade,
            heavy_charge=heavy_charge,
            free_shipping_threshold=free_shipping_threshold,
        )
        return factory.build()

    def build_enhanced_ecommerce_impression(
        self,
        list_name: Optional[EnhancedEcommerceListName],
        category_path: Optional[List[str]],
        position: int = 0,
        price_override: Optional[int] = None,
    ) -> EnhancedEcommerceImpressionView:
        """Build an `EnhancedEcommerceImpressionView` from the provided details"""
        factory = EnhancedEcommerceImpressionViewFactory(
            enabled_variants=self._enabled_variants,
            buybox_type=self._buybox_type,
            offer=None,
            platform=self._platform,
            event="eec.productImpressions",  # Yes, it's different from others here
        )
        return factory.build(
            list_name=list_name,
            category_path=category_path,
            position=position,
            price_override=price_override,
        )

    def build_enhanced_ecommerce_click(
        self,
        list_name: Optional[EnhancedEcommerceListName],
        category_path: Optional[List[str]],
        position: int = 0,
        quantity: int = 1,
        price_override: Optional[int] = None,
    ) -> EnhancedEcommerceClickView:
        """Build an `EnhancedEcommerceClickView` from the provided details"""
        factory = EnhancedEcommerceClickViewFactory(
            enabled_variants=self._enabled_variants,
            buybox_type=self._buybox_type,
            offer=None,
            platform=self._platform,
            event="productClick",
            include_currency=True,
            include_action=False,
        )
        return factory.build(
            list_name=list_name,
            category_path=category_path,
            position=position,
            quantity=quantity,
            price_override=price_override,
        )

    def build_enhanced_ecommerce_add_to_cart(
        self,
        category_path: Optional[List[str]],
        position: int = 0,
        quantity: int = 1,
        price_override: Optional[int] = None,
    ) -> EnhancedEcommerceAddToCartView:
        """Build an `EnhancedEcommerceAddToCartView` from the provided details"""
        factory = EnhancedEcommerceAddToCartViewFactory(
            enabled_variants=self._enabled_variants,
            buybox_type=self._buybox_type,
            offer=None,
            platform=self._platform,
            event="addToCart",
        )

        return factory.build(
            category_path=category_path,
            position=position,
            quantity=quantity,
            price_override=price_override,
        )
