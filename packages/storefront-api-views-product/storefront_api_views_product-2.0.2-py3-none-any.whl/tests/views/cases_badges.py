# flake8: noqa E501

from pytest_cases import parametrize
from storefront_product_adapter.models.buybox import BuyboxType

from storefront_api_views_product.views.badges import BadgesSummaryView, BadgesViewInfo
from storefront_api_views_product.views.models import BadgeType

URL_BASE = "https://media.takealot.com/promotions"
_NEXT_DAY_DELIVERY_BADGE_URL = (
    "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
)

next_day_badge0 = BadgesViewInfo(
    badge_id="badge-0",
    badge_type="image",
    badge_url_pattern=(
        "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
    ),
)
next_day_badge1 = BadgesViewInfo(
    badge_id="badge-1",
    badge_type="image",
    badge_url_pattern=(
        "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
    ),
)
next_day_badge2 = BadgesViewInfo(
    badge_id="badge-2",
    badge_type="image",
    badge_url_pattern=(
        "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
    ),
)


class SummaryBadgesViewCases:
    """
    Returns
    -------
        variants: Variant collection.
        buybox_type: BuyboxType
        expected: BadgesSummaryView
    """

    @parametrize(
        "buybox_type, expected_web, expected_app",
        [(BuyboxType.CUSTOM_1, "", "")],
    )
    def case_savings_only_upto_15(
        self,
        variants_badges_variants_savings_up_to_12_15,
        buybox_type,
        expected_web,
        expected_app,
    ):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="saving",
                    value="Up to 15% off",
                )
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="saving",
                    value="Up to 12% off",
                )
            ],
            promotion_id=None,
        )

        return (variants_badges_variants_savings_up_to_12_15, buybox_type, output)

    def case_savings_multi_promo(self, variants_badges_variants_savings_multi_promo):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="20% off"
                ),
                next_day_badge2,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="10% off"
                ),
                next_day_badge2,
            ],
            promotion_id=4,
        )
        return (
            variants_badges_variants_savings_multi_promo,
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_savings_promo_sold_out(
        self, variants_badges_variants_savings_soldout_promo
    ):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="sold_out", value="Deal Sold Out"
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="Up to 40% off"
                ),
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="sold_out", value="Deal Sold Out"
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="Up to 30% off"
                ),
            ],
            promotion_id=1,
        )

        return (
            variants_badges_variants_savings_soldout_promo,
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_toppick(self, variants_badges_variants_savings_toppick):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="top_pick", value="Top Pick"
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="20% off"
                ),
                next_day_badge2,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="top_pick", value="Top Pick"
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="10% off"
                ),
                next_day_badge2,
            ],
            promotion_id=123,
        )
        return (
            variants_badges_variants_savings_toppick,
            BuyboxType.CUSTOM_1,
            output,
        )


class SummaryExcludeBadgesViewCases:
    """
    Returns
    -------
        variants: Variant collection.
        exclude: Excluded types
        buybox_type: BuyboxType
        expected: BadgesSummaryView
    """

    def case_savings_only_upto_15_excl_savings(
        self, variants_badges_variants_savings_up_to_12_15
    ):
        output = BadgesSummaryView(
            entries=[],
            app_entries=[],
            promotion_id=None,
        )

        return (
            variants_badges_variants_savings_up_to_12_15,
            {BadgeType.SAVINGS},
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_savings_multi_promo_excl_savings(
        self, variants_badges_variants_savings_multi_promo
    ):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                ),
                next_day_badge1,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/varfour-{{view}}.png",
                ),
                next_day_badge1,
            ],
            promotion_id=4,
        )

        return (
            variants_badges_variants_savings_multi_promo,
            {BadgeType.SAVINGS},
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_savings_multi_promo_excl_image(
        self, variants_badges_variants_savings_multi_promo
    ):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="saving", value="20% off"
                ),
                next_day_badge1,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="saving", value="10% off"
                ),
                next_day_badge1,
            ],
            promotion_id=None,
        )

        return (
            variants_badges_variants_savings_multi_promo,
            {BadgeType.IMAGE},
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_savings_promo_sold_out_excl_sold_out(
        self, variants_badges_variants_savings_soldout_promo
    ):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="saving", value="Up to 40% off"
                )
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="saving", value="Up to 30% off"
                )
            ],
            promotion_id=None,
        )

        return (
            variants_badges_variants_savings_soldout_promo,
            {BadgeType.SOLD_OUT},
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_toppick_excl_top_pick(self, variants_badges_variants_savings_toppick):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/varonetwothree-{{view}}.png",
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="20% off"
                ),
                next_day_badge2,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/varonetwothree-{{view}}.png",
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="10% off"
                ),
                next_day_badge2,
            ],
            promotion_id=123,
        )

        return (
            variants_badges_variants_savings_toppick,
            {BadgeType.TOP_PICK},
            BuyboxType.CUSTOM_1,
            output,
        )

    def case_toppick_excl_top_pick_image(
        self, variants_badges_variants_savings_toppick
    ):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="saving", value="20% off"
                ),
                next_day_badge1,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0", badge_type="saving", value="10% off"
                ),
                next_day_badge1,
            ],
            promotion_id=None,
        )

        return (
            variants_badges_variants_savings_toppick,
            {BadgeType.IMAGE, BadgeType.TOP_PICK},
            BuyboxType.CUSTOM_1,
            output,
        )


class SummaryOnlyPromosBadgesViewCases:
    """
    Returns
    -------
        variants: Variant collection.
        only_promo_ids: Allowed promotion IDs.
        expected: BadgesSummaryView
    """

    def case_savings_multi_promo(self, variants_badges_variants_savings_multi_promo):
        output = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/vartwo-{{view}}.png",
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="20% off"
                ),
                next_day_badge2,
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="badge-0",
                    badge_type="image",
                    badge_url_pattern=f"{URL_BASE}/vartwo-{{view}}.png",
                ),
                BadgesViewInfo(
                    badge_id="badge-1", badge_type="saving", value="10% off"
                ),
                next_day_badge2,
            ],
            promotion_id=2,
        )

        return (variants_badges_variants_savings_multi_promo, (2, 3), output)


class SummaryViewToDictCases:
    """
    Returns
    -------
        badge_view_model: One model
        expected: Dict output
    """

    def case_all_fields_view_info(self):
        model = BadgesViewInfo(
            badge_id="qwe-rty",
            badge_type="a_type",
            badge_url_pattern="u://r.l",
            value="valval",
        )
        output = {
            "id": "qwe-rty",
            "type": "a_type",
            "badge_url_pattern": "u://r.l",
            "value": "valval",
        }
        return (model, output)

    def case_no_nones_view_info(self):
        model = BadgesViewInfo(badge_id="qwe-rty", badge_type="a_type")
        output = {
            "id": "qwe-rty",
            "type": "a_type",
        }
        return (model, output)

    def case_summary_view(self):
        model = BadgesSummaryView(
            entries=[
                BadgesViewInfo(
                    badge_id="qwe-rty",
                    badge_type="a_type",
                    badge_url_pattern="u://r.l",
                    value="valval",
                )
            ],
            app_entries=[
                BadgesViewInfo(
                    badge_id="qwe-rty",
                    badge_type="a_type",
                    badge_url_pattern="u://r.l",
                    value="valval",
                ),
                BadgesViewInfo(
                    badge_id="x",
                    badge_type="y",
                ),
            ],
        )

        output = {
            "entries": [
                {
                    "id": "qwe-rty",
                    "type": "a_type",
                    "badge_url_pattern": "u://r.l",
                    "value": "valval",
                }
            ],
            "app_entries": [
                {
                    "id": "qwe-rty",
                    "type": "a_type",
                    "badge_url_pattern": "u://r.l",
                    "value": "valval",
                },
                {"id": "x", "type": "y"},
            ],
            "promotion_id": None,
        }

        return (model, output)
