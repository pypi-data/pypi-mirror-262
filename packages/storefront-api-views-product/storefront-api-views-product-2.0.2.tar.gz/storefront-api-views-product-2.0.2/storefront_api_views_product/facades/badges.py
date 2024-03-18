from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Container, List, Optional

from storefront_media_urls.images.promotions import PromotionImages
from storefront_product_adapter.facades import PricingFacade, PromotionsFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition
from storefront_product_adapter.models.promotion import Promotion
from storefront_product_adapter.models.stock import OfferStockStatus, StockQuantity

from storefront_api_views_product.views.models import BadgeInfo, BadgeType

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import OfferAdapter
    from storefront_product_adapter.collections import VariantCollection


class BadgesFacade:
    """
    See docs/views/Badges.md for more details.
    """

    _NEXT_DAY_DELIVERY_BADGE_URL = (
        "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
    )

    def __init__(self, *, platform: Platform) -> None:
        self.platform = platform

    def get_pdp_badges_from_offer(
        self,
        *,
        offer: OfferAdapter,
        exclude_badge_types: Optional[Collection[BadgeType]] = None,
    ) -> List[BadgeInfo]:
        """
        PDP has no special scenarios where certain badges need to be excluded.

        SOLD_OUT and TOP_PICK are always excluded.
        """
        if not offer.availability.is_buyable():
            return []

        exclude_badges = set(exclude_badge_types or [])

        badges: List[BadgeInfo] = []

        if BadgeType.IMAGE not in exclude_badges:
            badge = self._get_image_badge_from_offer(offer)
            if badge:
                badges.append(badge)

        if BadgeType.SAVINGS not in exclude_badges:
            badge = self._get_savings_badge_from_offer(offer)
            if badge:
                badges.append(badge)

        if BadgeType.NEXT_DAY_DELIVERY not in exclude_badges:
            badge = self._get_next_day_delivery_badge_from_offer(offer)
            if badge:
                badges.append(badge)

        return badges

    def get_pdp_badges_from_variants(
        self,
        *,
        buyable_variants: VariantCollection,
        buybox_type: BuyboxType,
        exclude_badge_types: Optional[Collection[BadgeType]] = None,
    ) -> List[BadgeInfo]:
        """
        PDP has no special scenarios where certain badges need to be excluded.

        SOLD_OUT and TOP_PICK are always excluded.
        """
        badges: List[BadgeInfo] = []

        exclude_badges = set(exclude_badge_types or [])

        if BadgeType.IMAGE not in exclude_badges:
            badge = self._get_image_badge_from_variants(
                buyable_variants=buyable_variants
            )
            if badge:
                badges.append(badge)

        if BadgeType.SAVINGS not in exclude_badges:
            badge = self._get_savings_badge_from_variants(
                buyable_variants=buyable_variants,
                buybox_type=buybox_type,
            )
            if badge:
                badges.append(badge)

        return badges

    def get_summary_badges_from_variants(
        self,
        *,
        buyable_variants: VariantCollection,
        buybox_type: BuyboxType,
        exclude_badge_types: Optional[Collection[BadgeType]] = None,
        only_promo_ids: Optional[Container[int]] = None,
    ) -> List[BadgeInfo]:
        """
        Summary badges are for search and widget lists. In deals contexts some
        badges might be excluded by the caller. This function does not exclude
        any badge types by default.
        """
        badges: List[BadgeInfo] = []

        exclude_badges = set(exclude_badge_types or [])

        badge = self._get_promotion_badge_from_variants(
            buyable_variants,
            exclude_badge_types=exclude_badges,
            only_promo_ids=only_promo_ids,
        )
        if badge:
            badges.append(badge)

        if BadgeType.SAVINGS not in exclude_badges:
            badge = self._get_savings_badge_from_variants(
                buyable_variants=buyable_variants,
                buybox_type=buybox_type,
            )
            if badge:
                badges.append(badge)

        if BadgeType.NEXT_DAY_DELIVERY not in exclude_badges:
            badge = self._get_next_day_delivery_badge_from_variants(
                buyable_variants=buyable_variants,
                buybox_type=buybox_type,
            )
            if badge:
                badges.append(badge)

        return badges

    def _get_savings_badge_from_offer(self, offer: OfferAdapter) -> Optional[BadgeInfo]:
        savings_percentage = offer.get_savings_percentage(platform=self.platform)
        if not savings_percentage:
            # If 0%, we don't show it
            return None

        value = f"{savings_percentage}% off"
        return BadgeInfo(badge_type=BadgeType.SAVINGS, value=value)

    def _get_savings_badge_from_variants(
        self,
        buyable_variants: VariantCollection,
        buybox_type: BuyboxType,
    ) -> Optional[BadgeInfo]:
        # Don't consider used offers for savings badge
        pricing = PricingFacade(
            CollectionsFactory.pricing_from_variants(
                variants=buyable_variants,
                platform=self.platform,
                buybox_type=buybox_type,
                buybox_conditions_precedence=(OfferCondition.NEW,),
            )
        )
        savings_range = pricing.get_display_savings_range()
        if not savings_range:
            return None

        value = f"{savings_range.max}% off"
        if savings_range.min < savings_range.max:
            value = f"Up to {value}"

        return BadgeInfo(badge_type=BadgeType.SAVINGS, value=value)

    def _get_promotion_badge_from_winning_promotion(
        self, promotion: Promotion, exclude_badge_types: Container[BadgeType]
    ) -> Optional[BadgeInfo]:
        """
        Promotion badge is picked from a competing set of SOLD_OUT, TOP_PICK
        and PROMO_IMAGE, in that order.

        If a promotion is sold out, neither TOP_PICK nor PROMO_IMAGE will be allowed
        and SOLD_OUT will only be present if not excluded.
        """
        if not promotion.quantity:
            # Deal is sold out
            if BadgeType.SOLD_OUT in exclude_badge_types:
                # And we don't want to show the badge for it
                return None

            return BadgeInfo(
                badge_type=BadgeType.SOLD_OUT,
                value="Deal Sold Out",
                promotion_id=promotion.promotion_id,
            )

        is_top_pick = PromotionsFacade.is_top_pick(promotion)
        if is_top_pick and BadgeType.TOP_PICK not in exclude_badge_types:
            # It is a top pick and we are allowed to show the badge type
            return BadgeInfo(
                badge_type=BadgeType.TOP_PICK,
                value="Top Pick",
                promotion_id=promotion.promotion_id,
            )

        if BadgeType.IMAGE not in exclude_badge_types:
            # Last badge allowed is a promo_image type
            return self._get_image_badge_from_winning_promotion(promotion)

        return None

    def _get_image_badge_from_winning_promotion(
        self, promotion: Promotion
    ) -> Optional[BadgeInfo]:
        if not self._validate_promotion_slug(slug=promotion.slug):
            return None

        return BadgeInfo(
            badge_type=BadgeType.IMAGE,
            url_pattern=PromotionImages.build_badge_image_url(promotion.slug),
            promotion_id=promotion.promotion_id,
        )

    def _get_image_badge_from_offer(self, offer: OfferAdapter) -> Optional[BadgeInfo]:
        winning_promotion = offer.get_winning_promotion()
        if not winning_promotion:
            return None

        return self._get_image_badge_from_winning_promotion(promotion=winning_promotion)

    def _get_promotion_badge_from_variants(
        self,
        buyable_variants: VariantCollection,
        exclude_badge_types: Container[BadgeType],
        only_promo_ids: Optional[Container[int]],
    ) -> Optional[BadgeInfo]:
        winning_promotion = self._get_winning_promotion_from_variants(
            buyable_variants, only_promo_ids=only_promo_ids
        )

        if winning_promotion:
            return self._get_promotion_badge_from_winning_promotion(
                promotion=winning_promotion, exclude_badge_types=exclude_badge_types
            )

        if not winning_promotion and only_promo_ids:
            return BadgeInfo(
                badge_type=BadgeType.SOLD_OUT,
                value="Deal Sold Out",
                promotion_id=None,
            )

        return None

    def _get_image_badge_from_variants(
        self, buyable_variants: VariantCollection
    ) -> Optional[BadgeInfo]:
        winning_promotion = self._get_winning_promotion_from_variants(
            buyable_variants, only_promo_ids=None
        )
        if not winning_promotion:
            return None
        return self._get_image_badge_from_winning_promotion(promotion=winning_promotion)

    def _get_winning_promotion_from_variants(
        self,
        buyable_variants: VariantCollection,
        only_promo_ids: Optional[Container[int]],
    ) -> Optional[Promotion]:
        promotions: List[Promotion] = []
        for variant in buyable_variants:
            promotions.extend(
                filter(
                    None,
                    (
                        offer.get_winning_promotion(only_promo_ids=only_promo_ids)
                        for offer in variant.offers.values()
                        if offer.availability.is_buyable()
                    ),
                )
            )

        return PromotionsFacade.pick_winner_from_list(promotions)

    def _validate_promotion_slug(self, slug: Optional[str]) -> bool:
        return bool(slug and slug != "no-image-badge" and not slug.startswith("npd-"))

    def _get_next_day_delivery_badge_from_offer(
        self, offer: OfferAdapter
    ) -> Optional[BadgeInfo]:
        # should not return badge if offer is not in stock OR  if offer is pre-order
        if offer.get_stock_status() is not OfferStockStatus.IN_STOCK:
            return None

        # Display the badge on items that are in stock in all warehouses
        stock_quantities = offer.get_stock_quantities()
        if not self._has_stock_in_all_regions(stock_quantities):
            # One of the warehouses has no stock
            return None

        if offer.condition != OfferCondition.NEW:
            return None

        if offer.variant.productline.is_digital():
            return None

        # Do not display the badge on heavy/bulky items
        if bool(offer.variant.get_attribute_raw_value("has_heavy_charge")):
            return None

        return BadgeInfo(
            badge_type=BadgeType.IMAGE,
            url_pattern=self._NEXT_DAY_DELIVERY_BADGE_URL,
        )

    def _get_next_day_delivery_badge_from_variants(
        self,
        buyable_variants: VariantCollection,
        buybox_type: BuyboxType,
    ) -> Optional[BadgeInfo]:
        if len(buyable_variants) > 1:
            return None

        winning_offers = buyable_variants.get_winning_offers(
            platform=self.platform,
            buybox_type=buybox_type,
            buybox_condition=OfferCondition.NEW,
        )

        winner = winning_offers.get_singular()

        if winner is None:
            return None

        return self._get_next_day_delivery_badge_from_offer(winner)

    def _has_stock_in_all_regions(self, stock_quantity: StockQuantity) -> bool:
        """
        Simple method to determine whether stock is present in all regions.
        We treat having no regions as an item being out of stock.
        """
        if stock_quantity.warehouses_total == 0:
            return False

        if not stock_quantity.warehouse_regions:
            return False

        for region, quantity in stock_quantity.warehouse_regions.items():
            if quantity < 1:
                return False

        return True
