from __future__ import annotations

from typing import TYPE_CHECKING, Collection, List, Optional

from storefront_product_adapter.collections import VariantCollection
from storefront_product_adapter.facades.summary import SummaryFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform

from storefront_api_views_product.facades.buybox_preference import (
    BuyboxPreferenceFacade,
)

from .views.badges import BadgesSummaryView, BadgesSummaryViewFactory
from .views.buybox import BuyboxSummaryView, BuyboxSummaryViewFactory
from .views.core import CoreView, CoreViewFactory
from .views.enhanced_ecommerce import (
    EnhancedEcommerceAddToCartView,
    EnhancedEcommerceAddToCartViewFactory,
    EnhancedEcommerceClickView,
    EnhancedEcommerceClickViewFactory,
    EnhancedEcommerceImpressionView,
    EnhancedEcommerceImpressionViewFactory,
    EnhancedEcommerceListName,
)
from .views.gallery import GalleryView, GalleryViewFactory
from .views.models import BadgeType
from .views.promotions import PromotionsSummaryView, PromotionsSummaryViewFactory
from .views.reviews import ReviewsSummaryView, ReviewsSummaryViewFactory
from .views.stock_availability import (
    StockAvailabilitySummaryView,
    StockAvailabilitySummaryViewFactory,
)
from .views.variant import VariantSummaryView, VariantSummaryViewFactory

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import (
        OfferAdapter,
        ProductlineAdapter,
        VariantAdapter,
    )


class SummaryViewFactory:
    """
    A convenience factory used to create any summary based views for a given lineage.

    Mainly to be used for small card displays, like search results, recommendations
    and sponsored ads.

    For use in cart displays, this will likely need to take in a specific offer only,
    since that is the only thing that matters in a cart context.
    """

    _productline: ProductlineAdapter
    _enabled_variants: VariantCollection
    _buyable_variants: VariantCollection
    _selected_variant: Optional[VariantAdapter]
    _overall_winner: Optional[OfferAdapter]

    @classmethod
    def from_productline(
        cls, productline: ProductlineAdapter, *, buybox_type: Optional[BuyboxType]
    ) -> SummaryViewFactory:
        return cls(productline=productline, buybox_type=buybox_type)

    @classmethod
    def from_variants(
        cls, variants: VariantCollection, *, buybox_type: BuyboxType
    ) -> SummaryViewFactory:
        return cls(
            productline=variants.productline, buybox_type=buybox_type, variants=variants
        )

    @classmethod
    def from_variant(
        cls, variant: VariantAdapter, *, buybox_type: BuyboxType
    ) -> SummaryViewFactory:
        variants = VariantCollection(variant.productline)
        variants.add(variant_id=variant.variant_id, adapter=variant)
        return cls.from_variants(variants, buybox_type=buybox_type)

    def __init__(
        self,
        productline: ProductlineAdapter,
        *,
        buybox_type: Optional[BuyboxType],
        variants: Optional[VariantCollection] = None,
    ) -> None:
        """
        Take in a productline adapter and use the enabled and buyable variants from it.

        This factory does not take `platform` as a constructor parameter, since the
        views it builds are generally used in platform agnostic places. Whenever
        a summary view *does* use a specific platform, it will make that clear
        by having it as a required parameter without a default. The only views like
        this at the moment are the enhanced ecommerce views which callers are expected
        to set to WEB if they need to keep the Cat V1 behaviour.

        Parameters
        ----------
        productline:
            The productline adapter.
        buybox_type:
            The buybox type to use.
            * With OfferOpt disabled, Cat V2 must set this to CUSTOM_1.
            * With OfferOpt enabled, this should never be CUSTOM_1 and the value will
              only be used when the productline has a single enabled variant.

            The parameter can change to have a default of None once OfferOpt is fully
            rolled out. Until then, we need to make sure that callers are aware of
            the parameter and don't accidentally pick lowest_priced over custom_1
            when they are not supporting OfferOpt yet.

            Set this to None to let the library pick the default, which will currently
            always be `lowest_priced`. This effectively makes the parameter an override
            for OfferOpt callers that will likely never be used, since the only time
            a specific type is expected to be used is when the user selects one on the
            PDP. This factory does not build those views. Nonetheless, we will need
            this during the transition and may occasionally want to override it.
        """
        self._productline = productline
        if variants is not None:
            all_variants = variants
        else:
            all_variants = CollectionsFactory.variants_from_productline_adapter(
                productline
            )

        self._enabled_variants = all_variants.filter_by_availability(
            (AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE)
        )

        self._buyable_variants = self._enabled_variants.filter_by_availability(
            (AvailabilityStatus.BUYABLE,)
        )

        # Only get the SELECTED variant if you passed in a `VariantCollection`.
        # Without a collection we assume that you want to use productline
        # level information
        self._selected_variant = None
        if variants:
            self._selected_variant = self._buyable_variants.get_singular()
            if not self._selected_variant:
                self._selected_variant = self._enabled_variants.get_singular()

        # If we were given a buybox type that is offer-opt aware (not custom_1),
        # but we do not have a singular variant collection, force the default
        # (currently lowest_priced) to make sure PDP doesn't show different
        # prices based on offer_pref=fastest before a single variant is selected.
        if not buybox_type or (
            len(self._buyable_variants) != 1 and buybox_type != BuyboxType.CUSTOM_1
        ):
            buybox_type = BuyboxPreferenceFacade.get_default_for_variants(
                self._enabled_variants
            )
        self._buybox_type = buybox_type

        # Save a tiny bit of time by using buyable variants for the next step, since
        # we already had to filter by buyable for other methods.
        self._overall_winner = SummaryFacade.find_overall_offer_winner(
            variants=self._buyable_variants,
            buybox_type=buybox_type,
        )

    @property
    def offer_winner(self) -> Optional[OfferAdapter]:
        return self._overall_winner

    @property
    def selected_variant(self) -> Optional[VariantAdapter]:
        return self._selected_variant

    def build_core(self) -> CoreView:
        """Build a `CoreView` from the provided details"""
        factory = CoreViewFactory(
            productline=self._productline, variant=self._selected_variant
        )
        return factory.build()

    def build_badges(
        self,
        exclude_badge_types: Optional[Collection[BadgeType]] = None,
        promotion_ids: Optional[List[int]] = None,
    ) -> BadgesSummaryView:
        """Build a `BadgesSummaryView` from the provided details"""
        factory = BadgesSummaryViewFactory(
            buyable_variants=self._buyable_variants,
            buybox_type=self._buybox_type,
            exclude_badge_types=exclude_badge_types,
            only_promo_ids=promotion_ids,
        )
        return factory.build()

    def build_gallery(self) -> GalleryView:
        """Build a `GalleryView` from the provided details"""
        factory = GalleryViewFactory(
            productline=self._productline, variant=self._selected_variant
        )
        return factory.build()

    def build_promotions_summary(
        self, promotion_ids: Optional[List[int]] = None
    ) -> PromotionsSummaryView:
        """Build a `PromotionsSummaryView` from the provided details"""
        factory = PromotionsSummaryViewFactory(
            buyable_variants=self._buyable_variants,
            included_promotion_ids=promotion_ids,
        )
        return factory.build()

    def build_reviews_summary(self) -> ReviewsSummaryView:
        """Build a `ReviewsSummaryView` from the provided details"""
        factory = ReviewsSummaryViewFactory(productline=self._productline)
        return factory.build()

    def build_variant_summary(self) -> VariantSummaryView:
        """Build a `VariantSummaryView` from the provided details"""
        factory = VariantSummaryViewFactory(
            enabled_variants=self._enabled_variants,
        )
        return factory.build()

    def build_buybox_summary(
        self, *, heavy_charge: Optional[int] = None
    ) -> BuyboxSummaryView:
        """Build a `BuyboxSummaryView` from the provided details"""
        factory = BuyboxSummaryViewFactory.from_variants(
            buybox_type=self._buybox_type,
            enabled_variants=self._enabled_variants,
            heavy_charge=heavy_charge,
        )
        return factory.build()

    def build_stock_availability_summary(
        self, is_displayed: Optional[bool]
    ) -> StockAvailabilitySummaryView:
        """
        Build a `StockAvailabilitySummaryView` from the provided details

        Parameters
        ----------
        is_displayed:
            If set to True or False, a field called `is_displayed` will be included
            in the view with this value.
            If None, the field is omitted.
        """
        factory = StockAvailabilitySummaryViewFactory(
            buybox_type=self._buybox_type,
            enabled_variants=self._enabled_variants,
            specific_offer=None,
        )
        return factory.build(is_displayed=is_displayed)

    def build_enhanced_ecommerce_impression(
        self,
        platform: Platform,
        list_name: Optional[EnhancedEcommerceListName],
        category_path: Optional[List[str]],
        position: int = 0,
    ) -> EnhancedEcommerceImpressionView:
        """Build an `EnhancedEcommerceImpressionView` from the provided details"""
        factory = EnhancedEcommerceImpressionViewFactory(
            buybox_type=self._buybox_type,
            enabled_variants=self._enabled_variants,
            offer=self._overall_winner,
            platform=platform,
        )
        return factory.build(
            list_name=list_name, category_path=category_path, position=position
        )

    def build_enhanced_ecommerce_click(
        self,
        platform: Platform,
        list_name: Optional[EnhancedEcommerceListName],
        category_path: Optional[List[str]],
        position: int = 0,
    ) -> EnhancedEcommerceClickView:
        """Build an `EnhancedEcommerceClickView` from the provided details"""
        factory = EnhancedEcommerceClickViewFactory(
            buybox_type=self._buybox_type,
            enabled_variants=self._enabled_variants,
            offer=self._overall_winner,
            platform=platform,
        )
        return factory.build(
            list_name=list_name, category_path=category_path, position=position
        )

    def build_enhanced_ecommerce_add_to_cart(
        self,
        platform: Platform,
        category_path: Optional[List[str]],
        position: int = 0,
    ) -> EnhancedEcommerceAddToCartView:
        """Build an `EnhancedEcommerceAddToCartView` from the provided details"""
        factory = EnhancedEcommerceAddToCartViewFactory(
            buybox_type=self._buybox_type,
            enabled_variants=self._enabled_variants,
            offer=self._overall_winner,
            platform=platform,
        )
        return factory.build(category_path=category_path, position=position)
