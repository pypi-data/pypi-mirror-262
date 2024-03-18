import json

import pytest
from freezegun import freeze_time
from pytest_cases import parametrize_with_cases
from storefront_product_adapter.models.buybox import BuyboxType

from storefront_api_views_product.facades.badges import BadgesFacade
from storefront_api_views_product.views.badges import BadgesSummaryViewFactory
from storefront_api_views_product.views.models import BadgeInfo, BadgeType

from .cases_badges import (
    SummaryBadgesViewCases,
    SummaryExcludeBadgesViewCases,
    SummaryOnlyPromosBadgesViewCases,
    SummaryViewToDictCases,
)

pytestmark = pytest.mark.views

BADGES_MOMENT_IN_TIME = "2020-10-15T11:22:33+02:00"


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    ["variants", "buybox_type", "expected"], cases=SummaryBadgesViewCases
)
def test_factory_build(variants, buybox_type, expected):
    # === Setup ===
    factory = BadgesSummaryViewFactory(
        buyable_variants=variants, buybox_type=buybox_type
    )

    # === Execute ===
    output = factory.build()

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    ["variants", "exclude", "buybox_type", "expected"],
    cases=SummaryExcludeBadgesViewCases,
)
def test_factory_build_excludes(variants, exclude, buybox_type, expected):
    # === Setup ===
    factory = BadgesSummaryViewFactory(
        buyable_variants=variants, buybox_type=buybox_type, exclude_badge_types=exclude
    )

    # === Execute ===
    output = factory.build()

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    ["variants", "only_promo_ids", "expected"], cases=SummaryOnlyPromosBadgesViewCases
)
def test_factory_build_promotion_only(variants, only_promo_ids, expected):
    # === Setup ===
    factory = BadgesSummaryViewFactory(
        buyable_variants=variants,
        buybox_type=BuyboxType.CUSTOM_1,
        only_promo_ids=only_promo_ids,
    )

    # === Execute ===
    output = factory.build()

    # === Verify ===
    assert output == expected


@parametrize_with_cases(["model", "expected"], cases=SummaryViewToDictCases)
def test_view_to_dict(model, expected):
    # === Setup ===
    # === Execute ===
    output = model.to_dict()

    # === Verify ===
    assert output == expected
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


@freeze_time(BADGES_MOMENT_IN_TIME)
def test_get_badge_from_bad_promotions(mocker, variants_bad_promotions):
    from storefront_product_adapter.models.common import Platform

    facade = BadgesFacade(platform=Platform.WEB)
    output = facade.get_summary_badges_from_variants(
        buyable_variants=variants_bad_promotions,
        buybox_type=BuyboxType.CUSTOM_1,
        only_promo_ids=[],
    )

    assert output == [BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off")]
