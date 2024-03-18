import pytest
from pytest_cases import fixture, fixture_ref, parametrize
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform

from storefront_api_views_product import SummaryViewFactory
from storefront_api_views_product.views import (
    BadgesSummaryView,
    BuyboxSummaryView,
    CoreView,
    EnhancedEcommerceAddToCartView,
    EnhancedEcommerceClickView,
    EnhancedEcommerceImpressionView,
    GalleryView,
    PromotionsSummaryView,
    ReviewsSummaryView,
    StockAvailabilitySummaryView,
    VariantSummaryView,
)

pytestmark = pytest.mark.views


@fixture
def productline1(full_cat_doc_for_detail_test_only_one_variant):
    """
    This factory is not meant to contain much logic to begin with and the arguments
    passed to each sub-factory depends on that factory and could change.

    That leaves us with either testing full input and output or just testing that what
    the thing did is what it claimed to do and that the sub-factory did not change a
    return type. So for simplicity, just verify that returned objects are of the
    correct View type. We will at least pass in a real productline though.

    Downside is it's pretty much a complete catalogue document.
    """

    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_one_variant
    )


@fixture
def productline2(full_cat_doc_for_detail_test_only_two_variants):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_two_variants
    )


@fixture
def productline3(full_cat_doc_for_detail_test_only_one_variant_same_winner):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_one_variant_same_winner
    )


@fixture
def productline4(full_cat_doc_for_detail_test_only_one_variant_out_of_stock):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_one_variant_out_of_stock
    )


@fixture
def productline_disabled(full_cat_doc_for_detail_test_only_two_variants_disabled):
    """
    Test for in case something tries to build a view with a disabled productline.
    Normally these should just be skipped.
    """
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_two_variants_disabled
    )


@fixture
def productline_heavy(full_cat_doc_for_detail_test_only_two_variants_heavy):
    """
    Test for a buybox summary where a heavy delivery surcharge is applicable.
    """
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_two_variants_heavy
    )


@parametrize(
    "buybox_type, expected_buybox_type",
    [
        (BuyboxType.LOWEST_PRICED, BuyboxType.LOWEST_PRICED),
        (BuyboxType.FASTEST, BuyboxType.FASTEST),
        (BuyboxType.CUSTOM_1, BuyboxType.CUSTOM_1),
        (None, BuyboxType.LOWEST_PRICED),
    ],
)
def test_buybox_defaulting(productline1, buybox_type, expected_buybox_type):
    factory = SummaryViewFactory(productline1, buybox_type=buybox_type)
    assert factory._buybox_type == expected_buybox_type


def test_passing_in_variants_uses_those(productline2):
    factory = SummaryViewFactory(
        productline=productline2, buybox_type=BuyboxType.CUSTOM_1
    )
    # Baseline Check (variants are using the productline variants)
    assert factory._enabled_variants.get_ids() == [2222, 22221]

    variants = CollectionsFactory.variants_from_productline_adapter(productline2)
    variants = variants.filter_by_ids([2222])
    factory = SummaryViewFactory(
        productline=productline2, buybox_type=BuyboxType.CUSTOM_1, variants=variants
    )
    # Baseline Check (variants are using the productline variants)
    assert factory._enabled_variants.get_ids() == [2222]


def test_from_productline(productline2):
    factory = SummaryViewFactory.from_productline(
        productline2, buybox_type=BuyboxType.CUSTOM_1
    )
    assert isinstance(factory, SummaryViewFactory)
    assert factory._productline == productline2


def test_from_variants(productline2):
    variants = CollectionsFactory.variants_from_productline_adapter(productline2)
    variants = variants.filter_by_ids([2222])
    factory = SummaryViewFactory.from_variants(
        variants, buybox_type=BuyboxType.CUSTOM_1
    )
    assert isinstance(factory, SummaryViewFactory)
    assert factory._productline == productline2
    assert factory._enabled_variants.get_ids() == [2222]


def test_from_variant(productline2):
    variant = productline2.variants[2222]
    factory = SummaryViewFactory.from_variant(variant, buybox_type=BuyboxType.CUSTOM_1)
    assert isinstance(factory, SummaryViewFactory)
    assert factory._productline == productline2
    assert factory._enabled_variants.get_ids() == [2222]


def test_offer_winner(productline1):
    factory = SummaryViewFactory(productline1, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.offer_winner
    assert output and output.offer_id == 4444


def test_selected_variant(productline1):
    variant = productline1.variants[2222]
    factory = SummaryViewFactory.from_variant(variant, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.selected_variant
    assert output and output.variant_id == 2222


def test_selected_variant_for_non_buyable_only(productline4):
    variant = productline4.variants[2222]
    assert variant.availability == AvailabilityStatus.NON_BUYABLE

    factory = SummaryViewFactory.from_variant(variant, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.selected_variant
    assert output and output.variant_id == 2222


def test_selected_variant_does_not_apply_if_no_variants_passed(productline1):
    factory = SummaryViewFactory(productline1, buybox_type=BuyboxType.CUSTOM_1)
    assert factory.selected_variant is None


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_core(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_core()
    assert isinstance(output, CoreView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_badges(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_badges()
    assert isinstance(output, BadgesSummaryView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_gallery(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_gallery()
    assert isinstance(output, GalleryView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_promotions_summary(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_promotions_summary()
    assert isinstance(output, PromotionsSummaryView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_reviews_summary(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_reviews_summary()
    assert isinstance(output, ReviewsSummaryView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_variant_summary(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_variant_summary()
    assert isinstance(output, VariantSummaryView)


@parametrize(
    "buybox_type, heavy_charge, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, 100, [3001, 3223], [2882, 2993]),
        (BuyboxType.FASTEST, 1, [3001, 3223], [2882, 2993]),
        (None, 200, [3001, 3223], [2882, 2993]),
        (BuyboxType.CUSTOM_1, -1, [3002, 3223], [2883, 2992]),
    ],
)
def test_build_buybox_summary_with_heavy_charge(
    productline_heavy,
    heavy_charge,
    buybox_type,
    expected_web_prices,
    expected_app_prices,
):
    factory = SummaryViewFactory(productline_heavy, buybox_type=buybox_type)

    output = factory.build_buybox_summary(heavy_charge=heavy_charge)
    assert isinstance(output, BuyboxSummaryView)
    assert output.delivery_charges is not None
    assert output.delivery_charges.heavy_charge.cost == heavy_charge


@parametrize(
    "buybox_type, heavy_charge, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, None, [3001, 3223], [2882, 2993]),
        (BuyboxType.FASTEST, None, [3001, 3223], [2882, 2993]),
        (None, None, [3001, 3223], [2882, 2993]),
        (BuyboxType.CUSTOM_1, None, [3002, 3223], [2883, 2992]),
    ],
)
def test_build_buybox_summary_with_heavy_charge_but_heavy_charge_disabled(
    productline_heavy,
    heavy_charge,
    buybox_type,
    expected_web_prices,
    expected_app_prices,
):
    factory = SummaryViewFactory(productline_heavy, buybox_type=buybox_type)

    output = factory.build_buybox_summary(heavy_charge=heavy_charge)
    assert isinstance(output, BuyboxSummaryView)
    assert output.delivery_charges.heavy_charge is None


@parametrize(
    "buybox_type, heavy_charge, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, 200, [3001, 3223], [2882, 2993]),
        (BuyboxType.FASTEST, 99, [3001, 3223], [2882, 2993]),
        (None, None, [3001, 3223], [2882, 2993]),
        (BuyboxType.CUSTOM_1, None, [3002, 3223], [2883, 2992]),
    ],
)
def test_build_buybox_summary_without_heavy_charge_but_heavy_charge_enabled(
    productline2,
    heavy_charge,
    buybox_type,
    expected_web_prices,
    expected_app_prices,
):
    factory = SummaryViewFactory(productline2, buybox_type=buybox_type)

    output = factory.build_buybox_summary(heavy_charge=heavy_charge)
    assert isinstance(output, BuyboxSummaryView)
    assert output.delivery_charges.heavy_charge is None


@parametrize(
    "buybox_type, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, [3001, 3223], [2882, 2993]),
        (BuyboxType.FASTEST, [3001, 3223], [2882, 2993]),
        (None, [3001, 3223], [2882, 2993]),
        (BuyboxType.CUSTOM_1, [3002, 3223], [2883, 2992]),
    ],
)
def test_build_buybox_summary_variants(
    productline2, buybox_type, expected_web_prices, expected_app_prices
):
    factory = SummaryViewFactory(productline2, buybox_type=buybox_type)

    output = factory.build_buybox_summary()
    assert isinstance(output, BuyboxSummaryView)
    assert output.prices == expected_web_prices
    assert output.app_prices == expected_app_prices


@parametrize(
    "buybox_type, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, [3001, 3003], [2991, 2993]),
        (BuyboxType.FASTEST, [3001, 3003], [2991, 2993]),
        (None, [3001, 3003], [2991, 2993]),
        (BuyboxType.CUSTOM_1, [3002], [2992]),
    ],
)
def test_build_buybox_summary_one_variant_multi_winner(
    productline1, buybox_type, expected_web_prices, expected_app_prices
):
    factory = SummaryViewFactory(productline1, buybox_type=buybox_type)

    output = factory.build_buybox_summary()
    assert isinstance(output, BuyboxSummaryView)
    assert output.prices == expected_web_prices
    assert output.app_prices == expected_app_prices


@parametrize(
    "buybox_type, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, [3001], [2991]),
        (BuyboxType.FASTEST, [3001], [2991]),
        (BuyboxType.CUSTOM_1, [3002], [2992]),
        (None, [3001], [2991]),
    ],
)
def test_build_buybox_summary_one_variant_one_winner(
    productline3, buybox_type, expected_web_prices, expected_app_prices
):
    factory = SummaryViewFactory(productline3, buybox_type=buybox_type)

    output = factory.build_buybox_summary()
    assert isinstance(output, BuyboxSummaryView)
    assert output.prices == expected_web_prices
    assert output.app_prices == expected_app_prices


@parametrize(
    "buybox_type, expected_web_prices, expected_app_prices",
    [
        (BuyboxType.LOWEST_PRICED, [], []),
        (BuyboxType.FASTEST, [], []),
        (BuyboxType.CUSTOM_1, [], []),
        (None, [], []),
    ],
)
def test_build_buybox_summary_disabled(
    productline_disabled, buybox_type, expected_web_prices, expected_app_prices
):
    factory = SummaryViewFactory(productline_disabled, buybox_type=buybox_type)
    output = factory.build_buybox_summary()
    assert isinstance(output, BuyboxSummaryView)
    assert output.prices == expected_web_prices
    assert output.app_prices == expected_app_prices


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_stock_availability_summary(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_stock_availability_summary(is_displayed=None)
    assert isinstance(output, StockAvailabilitySummaryView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_enhanced_ecommerce_impression(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_enhanced_ecommerce_impression(
        platform=Platform.WEB,
        category_path=None,
        list_name=None,
    )
    assert isinstance(output, EnhancedEcommerceImpressionView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_enhanced_ecommerce_click(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_enhanced_ecommerce_click(
        platform=Platform.WEB,
        category_path=None,
        list_name=None,
    )
    assert isinstance(output, EnhancedEcommerceClickView)


@parametrize(
    "productline_input",
    [
        fixture_ref("productline1"),
        fixture_ref("productline_disabled"),
    ],
)
def test_build_enhanced_ecommerce_add_to_cart(productline_input):
    factory = SummaryViewFactory(productline_input, buybox_type=BuyboxType.CUSTOM_1)
    output = factory.build_enhanced_ecommerce_add_to_cart(
        platform=Platform.WEB,
        category_path=None,
    )
    assert isinstance(output, EnhancedEcommerceAddToCartView)
