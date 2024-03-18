import pytest
from freezegun import freeze_time
from pytest_cases import parametrize_with_cases
from storefront_product_adapter.adapters.offer import OfferAdapter
from storefront_product_adapter.models.common import Platform

from storefront_api_views_product.facades.badges import BadgesFacade
from storefront_api_views_product.views.models import BadgeInfo, BadgeType
from tests.conftest import BADGES_MOMENT_IN_TIME

from .cases_badges import (
    HasStockInAllRegionsCases,
    PdpBadgesExcludeFromOfferCases,
    PdpBadgesExcludeFromVariantsCases,
    PdpBadgesFromOfferCases,
    PdpBadgesFromVariantsCases,
    SummaryBadgesExcludeFromVariantsCases,
    SummaryBadgesFromVariantsCases,
)

pytestmark = pytest.mark.factories


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases("offer, platform, expected", cases=PdpBadgesFromOfferCases)
def test_pdp_badges_from_offer(mocker, offer, platform, expected):
    # === Setup ===
    facade = BadgesFacade(platform=platform)

    # === Execute ===
    output = facade.get_pdp_badges_from_offer(offer=offer)

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
def test_pdp_badges_from_digital_offer(mocker, offer_is_prepaid):
    # === Setup ===
    facade = BadgesFacade(platform=Platform.WEB)

    # === Execute ===
    output = facade.get_pdp_badges_from_offer(offer=offer_is_prepaid)

    # === Verify ===
    assert output == [BadgeInfo(badge_type=BadgeType.SAVINGS, value="20% off")]


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    "source, exclude, expected", cases=PdpBadgesExcludeFromOfferCases
)
def test_pdp_badges_exclude_from_offer(mocker, source, exclude, expected):
    # === Setup ===
    facade = BadgesFacade(platform=Platform.WEB)
    offer = OfferAdapter(parent=mocker.Mock(), source=source)

    # === Execute ===
    output = facade.get_pdp_badges_from_offer(offer=offer, exclude_badge_types=exclude)

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    "variants, platform, buybox_type, expected", cases=PdpBadgesFromVariantsCases
)
def test_pdp_badges_from_variants(variants, platform, buybox_type, expected):
    # === Setup ===
    facade = BadgesFacade(platform=platform)

    # === Execute ===
    output = facade.get_pdp_badges_from_variants(
        buyable_variants=variants,
        buybox_type=buybox_type,
    )

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    "variants, exclude, buybox_type, expected", cases=PdpBadgesExcludeFromVariantsCases
)
def test_pdp_badges_exclude_from_variants(
    mocker, variants, exclude, buybox_type, expected
):
    # === Setup ===
    facade = BadgesFacade(platform=Platform.WEB)

    # === Execute ===
    output = facade.get_pdp_badges_from_variants(
        buyable_variants=variants,
        buybox_type=buybox_type,
        exclude_badge_types=exclude,
    )

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    "variants, platform, buybox_type, expected, only_promo_ids",
    cases=SummaryBadgesFromVariantsCases,
)
def test_summary_badges_from_variants(
    mocker, variants, platform, buybox_type, expected, only_promo_ids
):
    # === Setup ===
    facade = BadgesFacade(platform=platform)

    # === Execute ===
    output = facade.get_summary_badges_from_variants(
        buyable_variants=variants,
        buybox_type=buybox_type,
        only_promo_ids=only_promo_ids,
    )

    # === Verify ===
    assert output == expected


@freeze_time(BADGES_MOMENT_IN_TIME)
@parametrize_with_cases(
    "variants, exclude, buybox_type, expected",
    cases=SummaryBadgesExcludeFromVariantsCases,
)
def test_summary_badges_exclude_from_variants(
    mocker, variants, exclude, buybox_type, expected
):
    # === Setup ===
    facade = BadgesFacade(platform=Platform.WEB)
    # === Execute ===
    output = facade.get_summary_badges_from_variants(
        buyable_variants=variants,
        buybox_type=buybox_type,
        exclude_badge_types=exclude,
    )

    # === Verify ===
    assert output == expected


@parametrize_with_cases(
    "stock_quantity, expected",
    cases=HasStockInAllRegionsCases,
)
def test_has_stock_in_all_regions(stock_quantity, expected, variants_bad_promotions):
    facade = BadgesFacade(platform=Platform.WEB)
    output = facade._has_stock_in_all_regions(stock_quantity)

    assert output == expected
