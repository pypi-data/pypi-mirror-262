# TODO: DSC-7685 - Post OfferOpt cleanup task:
# Change tests to favour LOWEST_PRICED instead of CUSTOM_1
from pytest_cases import parametrize
from storefront_product_adapter.adapters.offer import OfferAdapter
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition
from storefront_product_adapter.models.stock import StockQuantity

from storefront_api_views_product.views.models import BadgeInfo, BadgeType

URL_BASE = "https://media.takealot.com/promotions"
_NEXT_DAY_DELIVERY_BADGE_URL = (
    "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
)


class PdpBadgesExcludeFromOfferCases:
    """
    Exclude version of PdpBadgesFromOfferCases.case_promo_and_savings
    Returns
    -------
        offer_source: Offer schema source
        exclude: List of badge types to exclude
        expected: List of badges
    """

    def case_exclude_image(self, badges_offers_promo_and_savings_10_10):
        return (
            badges_offers_promo_and_savings_10_10,
            [BadgeType.IMAGE],
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off")],
        )

    def case_exclude_savings(self, badges_offers_promo_and_savings_10_10):
        return (
            badges_offers_promo_and_savings_10_10,
            [BadgeType.SAVINGS],
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/twotwo-{{view}}.png",
                    promotion_id=2,
                )
            ],
        )

    def case_exclude_both(self, badges_offers_promo_and_savings_10_10):
        return (
            badges_offers_promo_and_savings_10_10,
            [BadgeType.SAVINGS, BadgeType.IMAGE],
            [],
        )

    def case_exclude_next_day_delivery(self, badges_offers_promo_and_savings_10_10):
        return (
            badges_offers_promo_and_savings_10_10,
            [BadgeType.NEXT_DAY_DELIVERY],
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/twotwo-{{view}}.png",
                    promotion_id=2,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
            ],
        )

    def case_exclude_all_badges(self, badges_offers_promo_and_savings_10_10):
        return (
            badges_offers_promo_and_savings_10_10,
            [BadgeType.NEXT_DAY_DELIVERY, BadgeType.SAVINGS, BadgeType.IMAGE],
            [],
        )


class PdpBadgesFromOfferCases:
    """
    Returns
    -------
        offer: Offer adapter
        platform: Platform
        expected: List of badges
    """

    def case_savings_app_a(self, variant_not_prepaid, badges_offers_only_savings_12_23):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_savings_12_23
            ),
            Platform.APP,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="12% off")],
        )

    def case_savings_app_b(
        self, variant_not_prepaid, badges_offers_only_savings_app_12_0
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_savings_app_12_0
            ),
            Platform.APP,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="12% off")],
        )

    def case_savings_web_a(self, variant_not_prepaid, badges_offers_only_savings_12_23):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_savings_12_23
            ),
            Platform.WEB,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="23% off")],
        )

    def case_savings_web_b(
        self, variant_not_prepaid, badges_offers_only_savings_web_0_23
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_savings_web_0_23
            ),
            Platform.WEB,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="23% off")],
        )

    def case_savings_no_web(
        self, variant_not_prepaid, badges_offers_only_savings_app_12_0
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_savings_app_12_0
            ),
            Platform.WEB,
            [],
        )

    def case_savings_no_app(
        self, variant_not_prepaid, badges_offers_only_savings_web_0_23
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_savings_web_0_23
            ),
            Platform.APP,
            [],
        )

    @parametrize("platform", list(Platform))
    def case_non_buyable(
        self, platform, variant_not_prepaid, badges_offers_non_buyable
    ):
        return (
            OfferAdapter(parent=variant_not_prepaid, source=badges_offers_non_buyable),
            platform,
            [],
        )

    def case_promo_only(self, variant_not_prepaid, badges_offers_only_promo_0_0):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_only_promo_0_0
            ),
            Platform.WEB,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/oneone-{{view}}.png",
                    promotion_id=1,
                ),
            ],
        )

    def case_promo_and_savings(
        self, variant_not_prepaid, badges_offers_promo_and_savings_10_10
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid, source=badges_offers_promo_and_savings_10_10
            ),
            Platform.WEB,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/twotwo-{{view}}.png",
                    promotion_id=2,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
            ],
        )

    def case_promo_bad_slugs(
        self, variant_not_prepaid, badges_offers_only_bad_promo_slugs_0_0
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid,
                source=badges_offers_only_bad_promo_slugs_0_0,
            ),
            Platform.WEB,
            [],
        )

    def case_promo_and_savings_and_next_day(
        self, variant_not_prepaid_no_heavy_charge, offer_has_stock_in_all_warehouses
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid_no_heavy_charge,
                source=offer_has_stock_in_all_warehouses,
            ),
            Platform.WEB,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/twotwo-{{view}}.png",
                    promotion_id=2,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
                BadgeInfo(
                    badge_type=BadgeType.IMAGE, url_pattern=_NEXT_DAY_DELIVERY_BADGE_URL
                ),
            ],
        )

    def case_used_offer_has_no_next_day_delivery(
        self, variant_not_prepaid_no_heavy_charge, offer_has_stock_in_all_warehouses
    ):
        # Override condition, as used offers are not eligible for next day delivery
        offer_has_stock_in_all_warehouses["condition"] = OfferCondition.USED

        return (
            OfferAdapter(
                parent=variant_not_prepaid_no_heavy_charge,
                source=offer_has_stock_in_all_warehouses,
            ),
            Platform.WEB,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/twotwo-{{view}}.png",
                    promotion_id=2,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
            ],
        )

    def case_heavy_variant_has_no_next_day_delivery(
        self, variant_not_prepaid, offer_has_stock_in_all_warehouses
    ):
        return (
            OfferAdapter(
                parent=variant_not_prepaid,
                source=offer_has_stock_in_all_warehouses,
            ),
            Platform.WEB,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/twotwo-{{view}}.png",
                    promotion_id=2,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
            ],
        )


class PdpBadgesFromVariantsCases:
    """
    These cases also covers the scenario where the range min/max is expanded by offers
    that are not buybox winners. The variant range covers all offers, while display
    rules may only want a specific buybox winner of each variant in a collection to be
    considered. Perhaps the offers were also filtered out.

    Returns
    -------
        variants: Variant Collection
        platform: Platform
        buybox_type: BuyboxType
        expected: List of badges
    """

    @parametrize(
        "buybox_type, expected",
        [
            (BuyboxType.CUSTOM_1, "Up to 12% off"),
            (BuyboxType.FASTEST, "Up to 15% off"),
            (BuyboxType.LOWEST_PRICED, "Up to 10% off"),
        ],
    )
    def case_savings_only_app_upto_15(
        self, variant_badges_variants_savings_up_to_12_15, buybox_type, expected
    ):
        url_pattern = "https://media.takealot.com/promotions/oneone-{view}.png"
        return (
            variant_badges_variants_savings_up_to_12_15,
            Platform.APP,
            buybox_type,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    value=None,
                    url_pattern=url_pattern,
                    promotion_id=1,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value=expected),
            ],
        )

    @parametrize(
        "buybox_type, expected",
        [
            (BuyboxType.CUSTOM_1, "Up to 15% off"),
            (BuyboxType.FASTEST, "Up to 21% off"),
            (BuyboxType.LOWEST_PRICED, "Up to 23% off"),
        ],
    )
    def case_savings_only_web_upto_15(
        self, variant_badges_variants_savings_up_to_12_15, buybox_type, expected
    ):
        url_pattern = "https://media.takealot.com/promotions/oneone-{view}.png"
        return (
            variant_badges_variants_savings_up_to_12_15,
            Platform.WEB,
            buybox_type,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    value=None,
                    url_pattern=url_pattern,
                    promotion_id=1,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value=expected),
            ],
        )

    def case_savings_only_app_exactly_13(
        self, variants_badges_variants_savings_only_exactly_13_31
    ):
        return (
            variants_badges_variants_savings_only_exactly_13_31,
            Platform.APP,
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="13% off")],
        )

    def case_savings_only_web_exactly_31(
        self, variants_badges_variants_savings_only_exactly_13_31
    ):
        return (
            variants_badges_variants_savings_only_exactly_13_31,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="31% off")],
        )

    @parametrize("platform", list(Platform))
    def case_no_savings(self, platform, variants_badges_variants_no_savings):
        return (
            variants_badges_variants_no_savings,
            platform,
            BuyboxType.CUSTOM_1,
            [],
        )

    def case_savings_multi_promo_app(
        self, variants_badges_variants_savings_multi_promo
    ):
        return (
            variants_badges_variants_savings_multi_promo,
            Platform.APP,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
            ],
        )

    def case_savings_multi_promo_web(
        self, variants_badges_variants_savings_multi_promo
    ):
        return (
            variants_badges_variants_savings_multi_promo,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
            ],
        )

    def non_buyable_variant(self, variants_non_buyable):
        return (
            variants_non_buyable,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [],
        )


class PdpBadgesExcludeFromVariantsCases:
    """
    Returns
    -------
        variants: Variant collection.
        exclude: List of badge types to exclude.
        buybox_type: BuyboxType
        expected: List of badges
    """

    def case_exclude_savings_web(self, variants_badges_variants_savings_multi_promo):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.SAVINGS],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                )
            ],
        )

    def case_exclude_image_web(self, variants_badges_variants_savings_multi_promo):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.IMAGE],
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off")],
        )

    def case_exclude_both_web(self, variants_badges_variants_savings_multi_promo):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.SAVINGS, BadgeType.IMAGE],
            BuyboxType.CUSTOM_1,
            [],
        )


class SummaryBadgesFromVariantsCases:
    """
    The first group of tests are directly from PdpBadgesFromVariantsCases
    since those are expected to match.

    Returns
    -------
        variants: Variant collection.
        platform: Platform
        expected: List of badges
        only_promo_ids: List of promotion ids to filter on
    """

    def case_savings_only_app_upto_15(
        self, variants_badges_variants_savings_up_to_12_15
    ):
        url_pattern = "https://media.takealot.com/promotions/oneone-{view}.png"
        return (
            variants_badges_variants_savings_up_to_12_15,
            Platform.APP,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    value=None,
                    url_pattern=url_pattern,
                    promotion_id=1,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="Up to 12% off"),
            ],
            [],
        )

    def case_savings_only_web_upto_15(
        self, variants_badges_variants_savings_up_to_12_15
    ):
        url_pattern = "https://media.takealot.com/promotions/oneone-{view}.png"
        return (
            variants_badges_variants_savings_up_to_12_15,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    value=None,
                    url_pattern=url_pattern,
                    promotion_id=1,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="Up to 15% off"),
            ],
            [],
        )

    def case_savings_only_app_exactly_13(
        self, variants_badges_variants_savings_only_exactly_13_31
    ):
        return (
            variants_badges_variants_savings_only_exactly_13_31,
            Platform.APP,
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="13% off")],
            [],
        )

    def case_savings_only_web_exactly_31(
        self, variants_badges_variants_savings_only_exactly_13_31
    ):
        return (
            variants_badges_variants_savings_only_exactly_13_31,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="31% off")],
            [],
        )

    @parametrize("platform", list(Platform))
    def case_no_savings(self, platform, variants_badges_variants_no_savings):
        return (
            variants_badges_variants_no_savings,
            platform,
            BuyboxType.CUSTOM_1,
            [],
            [],
        )

    def case_savings_multi_promo_app(
        self, variants_badges_variants_savings_multi_promo
    ):
        return (
            variants_badges_variants_savings_multi_promo,
            Platform.APP,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="10% off"),
                BadgeInfo(
                    badge_type=BadgeType.IMAGE, url_pattern=_NEXT_DAY_DELIVERY_BADGE_URL
                ),
            ],
            [],
        )

    def case_savings_multi_promo_web(
        self, variants_badges_variants_savings_multi_promo
    ):
        return (
            variants_badges_variants_savings_multi_promo,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
                BadgeInfo(
                    badge_type=BadgeType.IMAGE, url_pattern=_NEXT_DAY_DELIVERY_BADGE_URL
                ),
            ],
            [],
        )

    def case_savings_multi_promo_web_digital_variants(
        self, variants_badges_digital_variants
    ):
        return (
            variants_badges_digital_variants,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
            ],
            [],
        )

    def case_savings_multi_promo_web_digital_variants_zero_savings_range(
        self, variants_badges_digital_variants_zero_savings_range
    ):
        return (
            variants_badges_digital_variants_zero_savings_range,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
            ],
            [],
        )

    def case_savings_promo_sold_out(
        self, variants_badges_variants_savings_soldout_promo
    ):
        return (
            variants_badges_variants_savings_soldout_promo,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.SOLD_OUT, value="Deal Sold Out", promotion_id=1
                ),
                BadgeInfo(
                    badge_type=BadgeType.SAVINGS,
                    value="Up to 40% off",
                    url_pattern=None,
                    promotion_id=None,
                ),
            ],
            [],
        )

    def case_toppick(self, variants_badges_variants_savings_toppick):
        return (
            variants_badges_variants_savings_toppick,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.TOP_PICK, value="Top Pick", promotion_id=123
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
            ],
            [],
        )

    def case_sold_out(self, variants_badges_no_promotion_offers):
        return (
            variants_badges_no_promotion_offers,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.SOLD_OUT,
                    value="Deal Sold Out",
                    url_pattern=None,
                    promotion_id=None,
                ),
                BadgeInfo(
                    badge_type=BadgeType.SAVINGS,
                    value="20% off",
                    url_pattern=None,
                    promotion_id=None,
                ),
            ],
            [123],
        )

    def case_custom_1_winner(self, variants_badges_two_winning_offers):
        return (
            variants_badges_two_winning_offers,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off")],
            [],
        )

    def case_two_variants(self, variants_badges_variants_savings_up_to_12_15):
        url_pattern = "https://media.takealot.com/promotions/oneone-{view}.png"
        return (
            variants_badges_variants_savings_up_to_12_15,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    value=None,
                    url_pattern=url_pattern,
                    promotion_id=1,
                ),
                BadgeInfo(
                    badge_type=BadgeType.SAVINGS,
                    value="Up to 15% off",
                    url_pattern=None,
                    promotion_id=None,
                ),
            ],
            [],
        )

    def case_out_of_stock(self, variants_non_buyable):
        return (variants_non_buyable, Platform.WEB, BuyboxType.CUSTOM_1, [], [])

    def case_live_preorder(self, variants_live_preorder):
        return (
            variants_live_preorder,
            Platform.WEB,
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off")],
            [],
        )


class SummaryBadgesExcludeFromVariantsCases:
    """
    Returns
    -------
        variants: Variant collection.
        exclude: List of badge types to exclude.
        expected: List of badges
    """

    def case_exclude_savings_web(self, variants_badges_variants_savings_multi_promo):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.SAVINGS],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(
                    badge_type=BadgeType.IMAGE, url_pattern=_NEXT_DAY_DELIVERY_BADGE_URL
                ),
            ],
        )

    def case_exclude_image_web(self, variants_badges_variants_savings_multi_promo):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.IMAGE],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
                BadgeInfo(
                    badge_type=BadgeType.IMAGE, url_pattern=_NEXT_DAY_DELIVERY_BADGE_URL
                ),
            ],
        )

    def case_exclude_savings_image_web(
        self, variants_badges_variants_savings_multi_promo
    ):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.SAVINGS, BadgeType.IMAGE],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE, url_pattern=_NEXT_DAY_DELIVERY_BADGE_URL
                )
            ],
        )

    def case_exclude_soldout_web(self, variants_badges_variants_savings_soldout_promo):
        return (
            variants_badges_variants_savings_soldout_promo,
            [BadgeType.SOLD_OUT],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="Up to 40% off"),
            ],
        )

    def case_exclude_toppick_web(self, variants_badges_variants_savings_toppick):
        return (
            variants_badges_variants_savings_toppick,
            [BadgeType.TOP_PICK],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varonetwothree-{{view}}.png",
                    promotion_id=123,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
            ],
        )

    def case_exclude_next_day_delivery(
        self, variants_badges_variants_savings_multi_promo
    ):
        return (
            variants_badges_variants_savings_multi_promo,
            [BadgeType.NEXT_DAY_DELIVERY],
            BuyboxType.CUSTOM_1,
            [
                BadgeInfo(
                    badge_type=BadgeType.IMAGE,
                    url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                    promotion_id=4,
                ),
                BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off"),
            ],
        )

    def case_digital_product(self, variants_digital_product):
        return (
            variants_digital_product,
            [],
            BuyboxType.CUSTOM_1,
            [BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off")],
        )


class HasStockInAllRegionsCases:
    """
    Returns
    -------
    stock_quantity: an offer's stock levels
    expected: the expected return value
    """

    def case_all_regions_have_stock(self):
        return (
            StockQuantity(
                warehouse_regions={"cpt": 1, "dbn": 1, "jhb": 1},
                warehouses_total=3,
                merchant=1,
            ),
            True,
        )

    def case_some_regions_have_stock(self):
        return (
            StockQuantity(
                warehouse_regions={"cpt": 0, "dbn": 1, "jhb": 1},
                warehouses_total=2,
                merchant=1,
            ),
            False,
        )

    def case_no_regions_have_stock(self):
        return (
            StockQuantity(
                warehouse_regions={"cpt": 0, "dbn": 0, "jhb": 0},
                warehouses_total=0,
                merchant=1,
            ),
            False,
        )

    def case_no_regions(self):
        return (
            StockQuantity(
                warehouse_regions={},
                warehouses_total=12,
                merchant=0,
            ),
            False,
        )
