from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from storefront_product_adapter.collections import VariantCollection
from storefront_product_adapter.facades.pricing import PricingFacade
from storefront_product_adapter.facades.summary import SummaryFacade
from storefront_product_adapter.factories.collections import (
    CollectionsFactory,
    PricingCollections,
)
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition
from storefront_product_adapter.models.pricing import PriceRange, SavingsRange
from storefront_product_adapter.models.promotion import PromotionGroup
from storefront_product_adapter.models.stock import PreOrderStatus

from storefront_api_views_product.errors import InvalidDataError
from storefront_api_views_product.utils.text import (
    create_pricing_string,
    create_promotion_quantity_string,
    create_savings_string,
    create_single_price_string,
)

from .models import BaseViewModel, InfoType, OfferPreference

if TYPE_CHECKING:
    from storefront_product_adapter.adapters.offer import OfferAdapter


BUYBOX_ICONS_BASE = "https://static.takealot.com/images/buybox-icons"


@dataclass
class BuyboxSummaryView(BaseViewModel):
    listing_price: Optional[int]
    pretty_price: str
    app_pretty_price: str
    prices: List[int]
    app_prices: List[int]
    saving: Optional[str]
    app_saving: Optional[str]
    is_add_to_cart_available: bool
    is_shop_all_options_available: bool
    is_add_to_wish_list_available: bool
    product_id: Optional[int]
    delivery_charges: DeliveryCharges
    tsin: Optional[int]
    is_preorder: bool
    add_to_cart_text: str
    promotion_qty: Optional[int]
    promotion_qty_display_text: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "listing_price": self.listing_price,
            "pretty_price": self.pretty_price,
            "app_pretty_price": self.app_pretty_price,
            "prices": self.prices,
            "app_prices": self.app_prices,
            "saving": self.saving,
            "app_saving": self.app_saving,
            "is_add_to_cart_available": self.is_add_to_cart_available,
            "is_shop_all_options_available": self.is_shop_all_options_available,
            "is_add_to_wish_list_available": self.is_add_to_wish_list_available,
            "product_id": self.product_id,
            "delivery_charges": self.delivery_charges.to_dict(),
            "tsin": self.tsin,
            "is_preorder": self.is_preorder,
            "add_to_cart_text": self.add_to_cart_text,
            "promotion_qty": self.promotion_qty,
            "promotion_qty_display_text": self.promotion_qty_display_text,
        }


@dataclass
class BuyboxDetailView(BaseViewModel):
    """
    All Optional fields will be omitted if None
    """

    plid: int
    buybox_items_type: BuyboxItemsType
    is_digital: bool
    items: List[BuyboxDetailItem]
    tsin: Optional[int]
    variants_call_to_action: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "plid": self.plid,
            "tsin": self.tsin,
            "variants_call_to_action": self.variants_call_to_action,
            "buybox_items_type": self.buybox_items_type.value,
            "is_digital": self.is_digital,
            "items": [item.to_dict() for item in self.items],
        }

        return self.drop_nones(data)


@dataclass
class BuyboxDetailItem(BaseViewModel):
    """
    All Optional fields will be omitted if None
    """

    is_selected: bool
    is_preorder: bool
    is_add_to_cart_available: bool
    is_add_to_wishlist_available: bool
    is_free_shipping_available: bool
    multibuy_display: bool
    delivery_charges: DeliveryCharges
    offer_detail: BuyboxOfferDetail
    sku: Optional[int]
    price: Optional[int]
    pretty_price: Optional[str]
    listing_price: Optional[int]
    add_to_cart_text: Optional[str]
    multibuy_label: Optional[str]
    bundle_label: Optional[str]
    promotion_qty: Optional[int]
    promotion_qty_display_text: Optional[str]
    sponsored_ads_seller_id: Optional[str]

    # The items below are best left in the Product BFF for now:
    #   * Moving all that here is just going to take too long.
    #   * Some of it is used in more than one place in the BFF and I'd rather move
    #     all in one go.
    #   * The Product BFF can add these manually. Not great, but good enough.
    loyalty_prices: Optional[List[BaseViewModel]] = None
    credit_options_summary: Optional[BaseViewModel] = None
    stock_availability: Optional[BaseViewModel] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "is_selected": self.is_selected,
            "is_preorder": self.is_preorder,
            "is_add_to_cart_available": self.is_add_to_cart_available,
            "is_add_to_wishlist_available": self.is_add_to_wishlist_available,
            "is_free_shipping_available": self.is_free_shipping_available,
            "multibuy_display": self.multibuy_display,
            "delivery_charges": self.delivery_charges.to_dict(),
            "offer_detail": self.offer_detail.to_dict(),
            "sku": self.sku,
            "price": self.price,
            "pretty_price": self.pretty_price,
            "listing_price": self.listing_price,
            "add_to_cart_text": self.add_to_cart_text,
            "multibuy_label": self.multibuy_label,
            "bundle_label": self.bundle_label,
            "promotion_qty": self.promotion_qty,
            "promotion_qty_display_text": self.promotion_qty_display_text,
            "sponsored_ads_seller_id": self.sponsored_ads_seller_id,
        }

        if self.loyalty_prices:
            data["loyalty_prices"] = [item.to_dict() for item in self.loyalty_prices]
        if self.credit_options_summary:
            data["credit_options_summary"] = self.credit_options_summary.to_dict()
        if self.stock_availability:
            data["stock_availability"] = self.stock_availability.to_dict()

        return self.drop_nones(data)


@dataclass
class BuyboxOfferDetail(BaseViewModel):
    display_text: Optional[str]
    preference: Optional[OfferPreference]
    icon_url: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "preference": self.preference.value if self.preference else None,
            "display_text": self.display_text,
            "icon_url": self.icon_url,
        }
        return self.drop_nones(data)


@dataclass
class HeavyCharge(BaseViewModel):
    cost: int
    info: str
    text: str
    info_type: InfoType = InfoType.SHORT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cost": self.cost,
            "info": self.info,
            "text": self.text,
            "info_type": self.info_type.value,
        }

    @classmethod
    def from_charge(cls, charge: int) -> HeavyCharge:
        info = f"A R {charge} heavy/bulky delivery surcharge applies to this item."
        text = f"+ R {charge} Delivery Surcharge"

        return HeavyCharge(cost=charge, info=info, text=text)


@dataclass
class DeliveryCharges(BaseViewModel):
    heavy_charge: Optional[HeavyCharge] = None

    def to_dict(self) -> Dict[str, Any]:
        if not self.heavy_charge:
            return {}

        return {"heavy_charge": self.heavy_charge.to_dict()}


class BuyboxItemsType(Enum):
    SUMMARY = "summary"
    SINGLE = "single"
    MULTI = "multi"


class _BuyboxBaseViewFactory:
    """
    Things common between the summary and detail views will be placed in this
    private class. Take care not to put something in here just because it _seems_
    similar. There are sometimes subtle differences.
    """

    TEXT_CTA_BTN_ADD_TO_CART = "Add to Cart"
    TEXT_CTA_BTN_PRE_ORDER = "Pre-order"

    DISPLAY_PROMOTION_QUANTITY_THRESHOLD: int = 20

    def __init__(
        self,
        *,
        enabled_variants: VariantCollection,
        heavy_charge: Optional[int] = None,
    ) -> None:
        self._productline = enabled_variants.productline
        self._enabled_variants = enabled_variants
        self._enabled_variant_count = len(enabled_variants)
        self._heavy_charge = heavy_charge
        self._has_heavy_charge_attribute = enabled_variants.any_has_true_attribute(
            "has_heavy_charge"
        )
        self._buyable_variants = enabled_variants.filter_by_availability(
            (AvailabilityStatus.BUYABLE,)
        )

    def _get_common_delivery_charge(self) -> DeliveryCharges:
        """
        Additional information to show related to delivery - currently only
        heavy_charge results in something to show here.
        """

        heavy_charge_item = None
        if self._heavy_charge and self._has_heavy_charge_attribute:
            heavy_charge_item = HeavyCharge.from_charge(self._heavy_charge)

        return DeliveryCharges(heavy_charge=heavy_charge_item)


class BuyboxSummaryViewFactory(_BuyboxBaseViewFactory):
    # Display promotion quantity if it is <= this value
    DISPLAY_LISTING_PRICE_THRESHOLD: int = 10

    @classmethod
    def from_variants(
        cls,
        *,
        buybox_type: BuyboxType,
        enabled_variants: VariantCollection,
        heavy_charge: Optional[int],
    ) -> BuyboxSummaryViewFactory:
        pricing_collections_web = CollectionsFactory.pricing_from_variants(
            variants=enabled_variants,
            platform=Platform.WEB,
            buybox_type=buybox_type,
            buybox_conditions_precedence=(OfferCondition.NEW, OfferCondition.USED),
        )
        pricing_collections_app = CollectionsFactory.pricing_from_variants(
            variants=enabled_variants,
            platform=Platform.APP,
            buybox_type=buybox_type,
            buybox_conditions_precedence=(OfferCondition.NEW, OfferCondition.USED),
        )

        buybox_type_pricing_web = PricingFacade(pricing_collections_web)
        buybox_type_pricing_app = PricingFacade(pricing_collections_app)

        savings_web = buybox_type_pricing_web.get_display_savings_range()
        savings_app = buybox_type_pricing_app.get_display_savings_range()

        # Assume the conditions of app and web winners will be the same
        if pricing_collections_app.offers.is_empty():
            offer_condition = OfferCondition.UNKNOWN
        else:
            offer_condition = next(
                iter(pricing_collections_app.offers.get_conditions())
            )

        if buybox_type == BuyboxType.CUSTOM_1:
            pricing_web = buybox_type_pricing_web.get_display_price_range()
            pricing_app = buybox_type_pricing_app.get_display_price_range()
            winner_count_app = len(pricing_collections_app.offers)
            winner_count_web = len(pricing_collections_web.offers)
        else:
            # We are in OfferOpt mode and need to get the price range from all
            # OfferOpt buybox type winners. We do NOT want to do this for savings range.
            all_winners_web = CollectionsFactory.offer_winners_for_buyboxes(
                platform=Platform.WEB,
                variants=enabled_variants,
                buybox_types=(BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST),
                buybox_conditions_precedence=(offer_condition,),
            )
            all_winners_app = CollectionsFactory.offer_winners_for_buyboxes(
                platform=Platform.APP,
                variants=enabled_variants,
                buybox_types=(BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST),
                buybox_conditions_precedence=(offer_condition,),
            )

            all_pricing_collections_web = PricingCollections(
                platform=Platform.WEB,
                buyable_variants=pricing_collections_web.buyable_variants,
                non_buyable_variants=pricing_collections_web.non_buyable_variants,
                offers=all_winners_web,
            )
            all_pricing_collections_app = PricingCollections(
                platform=Platform.APP,
                buyable_variants=pricing_collections_app.buyable_variants,
                non_buyable_variants=pricing_collections_app.non_buyable_variants,
                offers=all_winners_app,
            )

            pricing_web = PricingFacade(
                all_pricing_collections_web
            ).get_display_price_range()
            pricing_app = PricingFacade(
                all_pricing_collections_app
            ).get_display_price_range()
            winner_count_web = len(all_winners_web)
            winner_count_app = len(all_winners_app)

        # We want to pick the same offer as V1, but not use it for price range
        # narrowing. So only pick it after we got the pricing stuff. This concept
        # is a bit strange - picking an offer for a multi-variant multi-offer
        # productline.
        overall_offer = SummaryFacade.find_overall_offer_winner(
            variants=enabled_variants,
            buybox_type=buybox_type,
            buybox_conditions_precedence=(OfferCondition.NEW, OfferCondition.USED),
        )

        return BuyboxSummaryViewFactory(
            enabled_variants=enabled_variants,
            overall_offer=overall_offer,
            winner_count_app=winner_count_app,
            winner_count_web=winner_count_web,
            price_range_app=pricing_app,
            price_range_web=pricing_web,
            savings_range_app=savings_app,
            savings_range_web=savings_web,
            condition=offer_condition,
            heavy_charge=heavy_charge,
        )

    def __init__(
        self,
        *,
        enabled_variants: VariantCollection,
        overall_offer: Optional[OfferAdapter],
        winner_count_app: int,
        winner_count_web: int,
        price_range_app: Optional[PriceRange],
        price_range_web: Optional[PriceRange],
        savings_range_app: Optional[SavingsRange],
        savings_range_web: Optional[SavingsRange],
        condition: OfferCondition,
        heavy_charge: Optional[int] = None,
    ) -> None:
        super().__init__(enabled_variants=enabled_variants, heavy_charge=heavy_charge)

        self._offer = overall_offer
        self._winner_count_app = winner_count_app
        self._winner_count_web = winner_count_web
        self._price_range_app = price_range_app
        self._price_range_web = price_range_web
        self._savings_range_app = savings_range_app
        self._savings_range_web = savings_range_web
        self._condition = condition

    def build(self) -> BuyboxSummaryView:
        """
        Build and return a `BuyboxSummaryView` instance.
        """

        is_preorder = self._productline.get_preorder_status() == PreOrderStatus.LIVE
        add_to_cart_text = (
            self.TEXT_CTA_BTN_PRE_ORDER
            if is_preorder
            else self.TEXT_CTA_BTN_ADD_TO_CART
        )

        return BuyboxSummaryView(
            listing_price=self._get_listing_price(),
            pretty_price=create_pricing_string(self._price_range_web),
            app_pretty_price=create_pricing_string(self._price_range_app),
            prices=self._prices_as_list(self._price_range_web),
            app_prices=self._prices_as_list(self._price_range_app),
            saving=create_savings_string(self._savings_range_web),
            app_saving=create_savings_string(self._savings_range_app),
            is_add_to_cart_available=self._get_is_add_to_cart_available(),
            is_shop_all_options_available=self._get_is_shop_all_options_available(),
            is_add_to_wish_list_available=self._get_is_add_to_wishlist_available(),
            product_id=self._get_offer_id(),
            delivery_charges=self._get_common_delivery_charge(),
            tsin=self._get_variant_id(),
            is_preorder=is_preorder,
            add_to_cart_text=add_to_cart_text,
            promotion_qty=self._get_promotion_quantity(),
            promotion_qty_display_text=self._get_promotion_quantity_display_text(),
        )

    def _get_listing_price(self) -> Optional[int]:
        """
        Return the listing price for the given or picked offer.
        The library defines a theshold (`DISPLAY_LISTING_PRICE_THRESHOLD`) which will
        determine if the list price is worth showing.
        If there are multiple offers involved, we won't show a list price. The rule
        for V1 showing a list price for variants in search results is not clear. To
        keep it simple, we will only show it when Add to Cart is shown, in other words
        a single variant with a single buybox winner.
        After OfferOpt, if the cheapest and fastest offers are not the same, there
        are 2 buyable winners and no list price will be shown.
        """

        # Only show the list price on both platforms if we are certain it will have
        # the same value for both. Also only if there is one offer.
        if self._winner_count_app == 1 and self._winner_count_web == 1 and self._offer:
            list_price = self._offer.list_price
            selling_price = self._offer.get_selling_price(platform=Platform.WEB)
            if (
                list_price
                and selling_price
                and (list_price - selling_price) >= self.DISPLAY_LISTING_PRICE_THRESHOLD
            ):
                return int(list_price)

        return None

    def _get_offer_id(self) -> Optional[int]:
        """
        Return the offer_id for the given or picked offer.
        Even when there are multiple buyable winners, we still set this field to
        mimic V1 where we can.
        """

        if self._offer:
            return self._offer.offer_id

        return None

    @staticmethod
    def _prices_as_list(price_range: Optional[PriceRange]) -> List[int]:
        """
        This is needed only because the API schema uses a list.
        """
        if not price_range:
            return []

        return price_range.as_list()

    def _get_is_add_to_cart_available(self) -> bool:
        """
        We will show an Add to Cart button if there is a single buyable winning offer
        and the customer does not need to make any decision between variants or
        offer preference.
        This flag is also set for pre-orders that meet the above requirements.

        This flag is only used by Web at the moment. For Wishlist we need to revise
        this since we are platform aware there.
        TODO: CHSBE-xxxx
        """

        # To match V1, include out of stock variants in this check, not just buyables.
        return self._winner_count_web == 1 and self._enabled_variant_count == 1

    def _get_is_add_to_wishlist_available(self) -> bool:
        """
        A customer can add it to their wishlist if it is a single variant and not an
        unboxed offer.
        If there are only out of stock variants or only one in stock variant, a customer
        can still not add it to wishlist.
        If only one variant is enabled and all others are disabled, the product as a
        whole looks more like a single variant product and you can add it to wishlist.

        TODO: CHSBE-xxxx - the price/from-price shown in search will sometimes not
        match what the wishlist shows (lowest_priced vs custom_1) until we switch
        the wishlist to OfferOpt.
        """

        return (
            self._enabled_variant_count == 1 and self._condition != OfferCondition.USED
        )

    def _get_is_shop_all_options_available(self) -> bool:
        """
        This is True if the customer needs to make and kind of decision, such as
        selecting a variant or an offer preference.
        It is nearly the opposite of Add to Cart, except that no button is shown when
        there are no enabled variants to choose from.
        For a single variant productline, this will also be shown if the customer needs
        to choose between fastest and lowest priced offers.

        This flag is only used by Web at the moment. For Wishlist we need to revise
        this since we are platform aware there.
        TODO: CHSBE-xxxx
        """

        # To match V1, include out of stock variants in this check, not just buyables.
        if self._winner_count_web > 1:
            # Simple case, things to buy and choose
            return True

        if self._winner_count_web == 1:
            # Only one thing is still buyable, but there are variants to choose
            # from. This is weird, but match V1
            return self._enabled_variant_count > 1

        return False

    def _get_variant_id(self) -> Optional[int]:
        """
        Return the variant_id for the given or picked offer.
        Even when there is only a single variant at play, the field is only set
        if there is a buyable variant/offer. OK, we also set if for out of stock
        if there is only one variant.

        TODO: OfferOpt - we need a new rule for when there are two offers for a single
        variant. When fastest and cheapest winners of a single variant are different, we
        show Shop All Options so assume that we don't want to set this whenever we
        show Shop All Options. When all options are offers of the same variant, it
        could make sense to set this, but not the product_id. Discussions to be had.
        """

        single_variant = self._enabled_variants.get_singular()
        if single_variant:
            return single_variant.variant_id

        # To keep some old behaviour the same, fall back to the overall winning offer's
        # variant.
        if self._offer:
            return self._offer.variant.variant_id

        return None

    def _get_promotion_quantity(self) -> Optional[int]:
        """
        Get the number for "Only X left" displayed information.
        The library defines a theshold (`DISPLAY_PROMOTION_QUANTITY_THRESHOLD`) which
        will determine if the pill is worth showing.

        TODO: DSC-7890 - This may need to accept an applied promotions filter list so
        that this text is only shown in the context of the promotions applied. It must
        not look at only a single offer's promotions, but at all promotions.

        TODO: DSC-7434
        PromotionsFacade.get_active_offer_promotions - this should also take a promotion
        ID list.

        """

        # Keeping previous V2 behaviour for now (TODO DSC-7890), but using the App
        # winner count since the overall offer winner is App based as well.
        if self._winner_count_app != 1 or not self._offer:
            return None

        winning_promotion = self._offer.get_winning_promotion()
        if (
            winning_promotion
            and winning_promotion.quantity
            and winning_promotion.quantity <= self.DISPLAY_PROMOTION_QUANTITY_THRESHOLD
        ):
            return winning_promotion.quantity

        return None

    def _get_promotion_quantity_display_text(self) -> Optional[str]:
        """
        Return promotion quantity as a contextualised string, e.g. "Only 13 left"
        """

        return create_promotion_quantity_string(self._get_promotion_quantity())


class BuyboxDetailViewFactory(_BuyboxBaseViewFactory):
    """
    This factory is only meant for Offer Optimisation use.
    """

    _offer_detail_icons = {
        BuyboxType.FASTEST: f"{BUYBOX_ICONS_BASE}/fastest.png",
        BuyboxType.LOWEST_PRICED: f"{BUYBOX_ICONS_BASE}/lowest_priced.png",
    }

    def __init__(
        self,
        platform: Platform,
        buybox_type: BuyboxType,
        variants: VariantCollection,
        winning_offers: Dict[BuyboxType, OfferAdapter],
        pricing: PricingFacade,
        free_shipping_threshold: int,
        heavy_charge: Optional[float] = None,
    ):
        """
        This view factory will honour `buybox_type` for multi-variant collections.

        The Detail View factory will ensure that it is forced to the correct default
        when a single variant is not yet selected.

        Prameters
        ---------
        platform:
            Platform - affects prices
        buybox_type:
            Only used to mark the selected item
        variants:
            Multiple or single item variant collection, ideally of enabled variants.
            Can be only disabled variants, but the preferred usage is to first filter
            out all disabled variants. The higher level factory will do that.
        winning_offers:
            The order items were added to the dict will be the order they are displayed
            in. The caller must decide if they want to use the library controlled
            display order (should be always).
        pricing:
            To obtain pricing info, if any.
        free_shipping_threshold:
            Add free shipping info if minimum price >= threshold
        heavy_charge:
            The heavy charge cost (obtained from other service). If set, it will only be
            used if the variant collection has items that are marked as requiring heavy
            charge.
        """

        super().__init__(enabled_variants=variants, heavy_charge=int(heavy_charge or 0))

        self._platform = platform
        self._buybox_type = buybox_type
        self._winning_offers = winning_offers
        self._pricing = pricing
        self._free_shipping_threshold = free_shipping_threshold

        self._productline = variants.productline
        self._selected_variant = variants.get_singular()

        # The price_range can be None when there are only disabled variants
        self._price_range = self._pricing.get_display_price_range()

        # If this is OfferOpt AND we have more than one variant and therefore will
        # display a summary item, we should expand the price range similar to what
        # we do for the BuyboxSummary view. We won't consider out of stock
        # prices for this range.
        if (
            self._price_range
            and buybox_type != BuyboxType.CUSTOM_1
            and len(self._buyable_variants) > 1
        ):
            # We only want to expand the price range for the same condition as what
            # is in the given collections already. However, if there are multiple
            # condition types, we only want to expand with NEW offers - don't want
            # an Unboxed Deal to trigger a From Rx display when it won't show in the
            # main buybox.
            #
            # TODO: DSC-7891 - we want the higher level factory to be able to give
            # us a pricing facade that includes unboxed deals, but with some rules
            # applied.
            condition = next(iter(self._pricing.offer_conditions))

            all_winners = CollectionsFactory.offer_winners_for_buyboxes(
                platform=platform,
                variants=self._buyable_variants,
                buybox_types=(BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST),
                buybox_conditions_precedence=(condition,),
            )

            all_pricing_collections = PricingCollections(
                platform=platform,
                buyable_variants=self._buyable_variants,
                non_buyable_variants=VariantCollection(self._productline),
                offers=all_winners,
            )

            self._price_range.expand(
                PricingFacade(all_pricing_collections).get_display_price_range()
            )

    def build(self) -> BuyboxDetailView:
        items: List[BuyboxDetailItem] = []

        pricing_view_range = PriceRange(None, None)
        variants_call_to_action = None

        if self._selected_variant:
            if self._winning_offers:
                # The PricingCollections thing needs a bit of a revisit. For now,
                # just make sure that the price range on the top level is based on
                # these items.

                for buybox_type, offer in self._winning_offers.items():
                    item = self._build_offer_item(offer, buybox_type=buybox_type)
                    items.append(item)
                    pricing_view_range.expand(item.price)
            else:
                # Out of stock item content will look like a summary, but be marked
                # as SINGLE to make sure SUMMARY always implies that a frontend
                # can ignore things like stock availability.
                items.append(self._build_summary_item())

            if len(items) > 1:
                buybox_items_type = BuyboxItemsType.MULTI
            else:
                buybox_items_type = BuyboxItemsType.SINGLE
            tsin = self._selected_variant.variant_id
        else:
            buybox_items_type = BuyboxItemsType.SUMMARY
            if not self._enabled_variants.is_empty():
                variants_call_to_action = "Select an option"
            tsin = None
            items = [self._build_summary_item()]

        return BuyboxDetailView(
            plid=self._productline.productline_id,
            buybox_items_type=buybox_items_type,
            is_digital=self._productline.is_digital(),
            tsin=tsin,
            variants_call_to_action=variants_call_to_action,
            items=items,
        )

    def _build_summary_item(self) -> BuyboxDetailItem:
        add_to_cart_text = self.TEXT_CTA_BTN_ADD_TO_CART

        # Summary item: Either multi-variant or out of stock, cannot be pre-order.
        # Catalogue marks pre-order offers as buyable
        is_preorder = False

        return BuyboxDetailItem(
            # We promised frontends that one item will always be selected, so
            # select this even though it's a summary item.
            is_selected=True,
            sku=None,
            price=self._price_range.min if self._price_range else None,
            pretty_price=create_pricing_string(self._price_range) or None,
            add_to_cart_text=add_to_cart_text,
            is_add_to_wishlist_available=self._can_add_to_wishlist(),
            is_free_shipping_available=self._has_free_shipping(),
            is_preorder=is_preorder,
            delivery_charges=self._get_common_delivery_charge(),
            # All items below do not apply for a summary item
            listing_price=None,  # Only shown when buyable offer
            offer_detail=BuyboxOfferDetail(
                display_text=None, preference=None, icon_url=None
            ),
            is_add_to_cart_available=False,  # Summary item, can't buy yet
            multibuy_display=False,
            multibuy_label=None,
            bundle_label=None,
            promotion_qty=None,
            promotion_qty_display_text=None,
            sponsored_ads_seller_id=None,
            # The Product BFF needs to set these for now
            loyalty_prices=None,
            credit_options_summary=None,
            stock_availability=None,
        )

    def _build_offer_item(
        self, offer: OfferAdapter, buybox_type: BuyboxType
    ) -> BuyboxDetailItem:
        if not offer.availability.is_buyable():
            raise InvalidDataError(
                f"PLID{self._productline.productline_id} offer {offer.offer_id} "
                "is not buyable"
            )

        add_to_cart_text = self.TEXT_CTA_BTN_ADD_TO_CART
        is_preorder = self._productline.get_preorder_status() == PreOrderStatus.LIVE
        if is_preorder:
            add_to_cart_text = self.TEXT_CTA_BTN_PRE_ORDER

        price = offer.get_selling_price(platform=self._platform)
        if not price:
            raise InvalidDataError(
                f"PLID{self._productline.productline_id} offer {offer.offer_id} "
                "has no selling price"
            )

        multi_buy = self._get_multibuy_label(offer)
        bundle_label = self._get_bundle_label(offer)
        promo_qty, promo_text = self._get_promotion_quantity(offer)

        return BuyboxDetailItem(
            is_selected=buybox_type == self._buybox_type,
            sku=offer.offer_id,
            price=price,
            pretty_price=create_single_price_string(price),
            add_to_cart_text=add_to_cart_text,
            is_add_to_wishlist_available=self._can_add_to_wishlist(),
            is_free_shipping_available=self._has_free_shipping(),
            is_preorder=is_preorder,
            delivery_charges=self._get_common_delivery_charge(),
            # All items below do not apply for a summary item
            listing_price=int(offer.list_price),
            offer_detail=self._build_offer_detail(buybox_type),
            is_add_to_cart_available=True,
            multibuy_display=bool(multi_buy),
            multibuy_label=multi_buy,
            bundle_label=bundle_label,
            promotion_qty=promo_qty,
            promotion_qty_display_text=promo_text,
            sponsored_ads_seller_id=self._get_sponsored_ads_seller_id(offer),
            # The Product BFF needs to set these for now
            loyalty_prices=None,
            credit_options_summary=None,
            stock_availability=None,
        )

    def _can_add_to_wishlist(self) -> bool:
        """
        Similar to search, but a little more focussed on specific user selection.
        Can only add to wish list when there is a specific variant selected and then
        only if it is not a used offer.
        """

        if not self._selected_variant:
            return False

        # Out of stock will not have any conditions. We only want to prevent wishlist
        # of unboxed winners.
        return OfferCondition.USED not in self._pricing.offer_conditions

    def _has_free_shipping(self) -> bool:
        if self._productline.is_digital():
            return False

        if self._price_range and self._price_range.min >= self._free_shipping_threshold:
            return not self._has_heavy_charge_attribute

        return False

    def _build_offer_detail(self, buybox_type: BuyboxType) -> BuyboxOfferDetail:
        offer_pref = OfferPreference.from_buybox_type(buybox_type)

        display_text: Optional[str] = None
        if offer_pref == OfferPreference.FASTEST:
            display_text = "Fastest Delivery"
        else:  # Only two enum options at present
            display_text = "Best Price"

        return BuyboxOfferDetail(
            display_text=display_text,
            preference=offer_pref,
            icon_url=self._offer_detail_icons.get(buybox_type),
        )

    def _get_multibuy_label(self, offer: OfferAdapter) -> Optional[str]:
        promos = offer.get_promotions()
        multibuys = [p for p in promos if p.group == PromotionGroup.MULTI_BUY]
        if len(multibuys) > 1:
            return "Save with Bundle Deals"
        elif len(multibuys) == 1:
            return multibuys[0].display_name

        return None

    def _get_bundle_label(self, offer: OfferAdapter) -> Optional[str]:
        promos = offer.get_promotions()
        bundles = [p for p in promos if p.group and p.group.is_bundle()]
        if len(bundles) > 1:
            return f"Save with Bundle Deals ({len(bundles)})"
        elif bundles:
            return bundles[0].display_name

        return None

    def _get_promotion_quantity(
        self,
        offer: OfferAdapter,
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Get the promotion quantity and the display text if the selected offer is
        currently on a promotion (with limited quantity available).

        Returns a tuple containing quantity, message
        """

        promotion = offer.get_winning_promotion()
        if not promotion:
            return None, None

        if (
            promotion.group == PromotionGroup.APP_ONLY_DEAL
            and self._platform == Platform.APP
        ):
            # Do not return APP-ONLY deals to Non-App platforms
            return None, None

        slug = promotion.slug or ""
        quantity = promotion.quantity or 0

        if (
            slug and slug.startswith("npd-")
        ) or quantity > self.DISPLAY_PROMOTION_QUANTITY_THRESHOLD:
            return None, None

        message = create_promotion_quantity_string(quantity)

        return quantity, message

    def _get_sponsored_ads_seller_id(
        self,
        offer: OfferAdapter,
    ) -> str:
        """
        Return the seller/supplier ID for the purposes of OnlineSales events
        """

        prefix = "R"  # Default - Retail
        if offer.is_marketplace_offer():
            prefix = "M"

        merchant = offer.get_merchant()

        return f"{prefix}{merchant.merchant_id}"
