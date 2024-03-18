import pytest
from pytest_cases import fixture, parametrize
from storefront_product_adapter.collections.variant import VariantCollection
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform

from storefront_api_views_product import DetailViewFactory
from storefront_api_views_product.errors import ViewConfigurationError

pytestmark = pytest.mark.views


@fixture
def productline_one_variant(full_cat_doc_for_detail_test_only_one_variant):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_one_variant
    )


@fixture
def productline_two_variants(full_cat_doc_for_detail_test_only_two_variants):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_two_variants
    )


@fixture
def productline_used_only(full_cat_doc_for_detail_test_one_variant_used_only):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_one_variant_used_only
    )


@fixture
def productline_one_variant_same_winner(
    full_cat_doc_for_detail_test_only_one_variant_same_winner,
):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_one_variant_same_winner
    )


@fixture
def productline_out_of_stock(
    full_cat_doc_for_detail_test_only_one_variant_out_of_stock,
):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_one_variant_out_of_stock
    )


@fixture
def productline_variants_disabled(
    full_cat_doc_for_detail_test_only_two_variants_disabled,
):
    return AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_two_variants_disabled
    )


@fixture
def variants_one_variant(productline_one_variant):
    return CollectionsFactory.variants_from_productline_adapter(productline_one_variant)


@parametrize("platform", list(Platform))
@parametrize(
    "buybox_type, expected_buybox_type",
    [
        (BuyboxType.LOWEST_PRICED, BuyboxType.LOWEST_PRICED),
        (BuyboxType.FASTEST, BuyboxType.FASTEST),
        (BuyboxType.CUSTOM_1, BuyboxType.CUSTOM_1),
        (None, BuyboxType.LOWEST_PRICED),
    ],
)
def test_factory_init_variants(
    variants_one_variant, platform, buybox_type, expected_buybox_type
):
    factory = DetailViewFactory(
        platform=platform,
        buybox_type=buybox_type,
        enabled_variants=variants_one_variant,
    )

    assert factory._buybox_type == expected_buybox_type
    assert factory._platform == platform


def test_factory_init_empty_requireds():
    with pytest.raises(ViewConfigurationError):
        DetailViewFactory(platform=Platform.APP, buybox_type=None)


def test_factory_init_both_requireds(mocker):
    with pytest.raises(ViewConfigurationError):
        DetailViewFactory(
            platform=Platform.APP,
            buybox_type=None,
            productline=mocker.Mock(),
            enabled_variants=mocker.Mock(),
        )


def test_factory_init_empty_collection_no_exception(mocker):
    DetailViewFactory(
        platform=Platform.APP,
        buybox_type=None,
        enabled_variants=VariantCollection(mocker.Mock()),
    )


@parametrize("platform", list(Platform))
@parametrize(
    "buybox_type, expected_buybox_type",
    [
        (BuyboxType.LOWEST_PRICED, BuyboxType.LOWEST_PRICED),
        (BuyboxType.FASTEST, BuyboxType.FASTEST),
        (BuyboxType.CUSTOM_1, BuyboxType.CUSTOM_1),
        (None, BuyboxType.LOWEST_PRICED),
    ],
)
def test_factory_init_productline(
    productline_one_variant, platform, buybox_type, expected_buybox_type
):
    factory = DetailViewFactory(
        platform=platform, buybox_type=buybox_type, productline=productline_one_variant
    )

    # These asserts are not really useful now, but later when we have OfferOpt
    # defaulting logic and single winners etc. it will
    assert factory._buybox_type == expected_buybox_type
    assert factory._platform == platform


def test_factory_init_productline_one_variant_default_buybox(productline_one_variant):
    """
    Tests some internal state
    """

    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_one_variant,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant.variant_id == 2222
    assert factory.winning_offers[BuyboxType.LOWEST_PRICED].offer_id == 5555
    assert factory.winning_offers[BuyboxType.FASTEST].offer_id == 3333


def test_factory_init_productline_used_only_default_buybox(productline_used_only):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_used_only,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant.variant_id == 2222
    assert factory.winning_offers[BuyboxType.LOWEST_PRICED].offer_id == 6666


def test_factory_init_productline_two_variants_default_buybox(productline_two_variants):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_two_variants,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant is None
    assert factory.winning_offers == {}


def test_factory_init_variants_one_variant(variants_one_variant):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        enabled_variants=variants_one_variant,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant.variant_id == 2222
    assert factory.winning_offers[BuyboxType.LOWEST_PRICED].offer_id == 5555
    assert factory.winning_offers[BuyboxType.FASTEST].offer_id == 3333


def test_factory_init_bad_params():
    with pytest.raises(ViewConfigurationError):
        DetailViewFactory(platform=Platform.WEB, buybox_type=None)


@parametrize("buybox_type", [BuyboxType.FASTEST, BuyboxType.LOWEST_PRICED])
def test_factory_init_productline_one_variant_specific_buybox(
    productline_one_variant, buybox_type
):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        productline=productline_one_variant,
        buybox_type=buybox_type,
    )

    assert factory._buybox_type == buybox_type
    assert factory._platform == Platform.WEB
    assert factory._selected_variant.variant_id == 2222
    assert factory.winning_offers[BuyboxType.LOWEST_PRICED].offer_id == 5555
    assert factory.winning_offers[BuyboxType.FASTEST].offer_id == 3333


def test_factory_init_productline_one_variant_same_winner(
    productline_one_variant_same_winner,
):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_one_variant_same_winner,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant.variant_id == 2222
    assert factory.winning_offers[BuyboxType.LOWEST_PRICED].offer_id == 5555


def test_factory_init_productline_out_of_stock(productline_out_of_stock):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_out_of_stock,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant.variant_id == 2222
    assert factory.winning_offers == {}


def test_factory_init_productline_variants_disabled(productline_variants_disabled):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_variants_disabled,
    )

    assert factory._buybox_type == BuyboxType.LOWEST_PRICED
    assert factory._platform == Platform.WEB
    assert factory._selected_variant is None
    assert factory.winning_offers == {}


def test_build_buybox(productline_one_variant_same_winner):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_one_variant_same_winner,
    )

    output = factory.build_buybox(free_shipping_threshold=111, heavy_charge=222)

    icon_url = "https://static.takealot.com/images/buybox-icons/lowest_priced.png"

    assert output.to_dict() == {
        "plid": 1111,
        "tsin": 2222,
        "buybox_items_type": "single",
        "is_digital": False,
        "items": [
            {
                "is_selected": True,
                "is_preorder": False,
                "is_add_to_cart_available": True,
                "is_add_to_wishlist_available": True,
                "is_free_shipping_available": True,
                "multibuy_display": False,
                "delivery_charges": {},
                "offer_detail": {
                    "preference": "lowest_priced",
                    "display_text": "Best Price",
                    "icon_url": icon_url,
                },
                "sku": 5555,
                "price": 3001,
                "pretty_price": "R 3,001",
                "listing_price": 4004,
                "add_to_cart_text": "Add to Cart",
                "sponsored_ads_seller_id": "R345",
            }
        ],
    }


def test_build_buybox_all_disabled(productline_variants_disabled):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=None,
        productline=productline_variants_disabled,
    )

    output = factory.build_buybox(free_shipping_threshold=111, heavy_charge=222)

    assert output.to_dict() == {
        "plid": 1111,
        "buybox_items_type": "summary",
        "is_digital": False,
        "items": [
            {
                "is_selected": True,
                "is_preorder": False,
                "is_add_to_cart_available": False,
                "is_add_to_wishlist_available": False,
                "is_free_shipping_available": False,
                "multibuy_display": False,
                "delivery_charges": {},
                "offer_detail": {},
                "add_to_cart_text": "Add to Cart",
            }
        ],
    }


@parametrize(
    "quantity, expected_quantity",
    [
        (..., 1),
        (0, 0),
        (32, 32),
    ],
)
@parametrize(
    "buybox_type, price_override, expected_price, expected_offer",
    [
        (BuyboxType.CUSTOM_1, None, 3002, 4444),
        (BuyboxType.CUSTOM_1, 8866, 8866, 4444),
        (BuyboxType.LOWEST_PRICED, None, 3001, 5555),
        (BuyboxType.LOWEST_PRICED, 8866, 8866, 5555),
        (BuyboxType.FASTEST, None, 3003, 3333),
        (BuyboxType.FASTEST, 8866, 8866, 3333),
    ],
)
def test_build_enhanced_ecommerce_click(
    productline_one_variant,
    buybox_type,
    price_override,
    expected_price,
    expected_offer,
    quantity,
    expected_quantity,
):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=buybox_type,
        productline=productline_one_variant,
    )

    kwargs = {}
    if quantity is not ...:
        kwargs["quantity"] = quantity

    output = factory.build_enhanced_ecommerce_click(
        category_path=None,
        list_name=None,
        price_override=price_override,
        **kwargs,
    )

    assert output.to_dict() == {
        "event": "productClick",
        "ecommerce": {
            "click": {
                "actionField": {},
                "products": [
                    {
                        "id": "PLID1111",
                        "name": "Productline Title 1111",
                        "brand": "Summarisor",
                        "category": "",
                        "variant": None,
                        "dimension1": None,
                        "dimension2": expected_offer,
                        "price": expected_price,
                        "quantity": expected_quantity,
                        "position": 0,
                    }
                ],
            },
            "currencyCode": "ZAR",
        },
    }


@parametrize(
    "buybox_type, price_override, expected_price, expected_offer",
    [
        (BuyboxType.CUSTOM_1, None, 3002, 4444),
        (BuyboxType.CUSTOM_1, 8866, 8866, 4444),
        (BuyboxType.LOWEST_PRICED, None, 3001, 5555),
        (BuyboxType.LOWEST_PRICED, 8866, 8866, 5555),
        (BuyboxType.FASTEST, None, 3003, 3333),
        (BuyboxType.FASTEST, 8866, 8866, 3333),
    ],
)
def test_build_enhanced_ecommerce_impression(
    productline_one_variant, buybox_type, price_override, expected_price, expected_offer
):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=buybox_type,
        productline=productline_one_variant,
    )

    output = factory.build_enhanced_ecommerce_impression(
        category_path=None,
        list_name=None,
        price_override=price_override,
    )

    assert output.to_dict() == {
        "event": "eec.productImpressions",
        "ecommerce": {
            "currencyCode": "ZAR",
            "impressions": [
                {
                    "id": "PLID1111",
                    "name": "Productline Title 1111",
                    "brand": "Summarisor",
                    "category": "",
                    "variant": None,
                    "dimension1": None,
                    "dimension2": expected_offer,
                    "price": expected_price,
                    "position": 0,
                }
            ],
        },
    }


@parametrize(
    "quantity, expected_quantity",
    [
        (..., 1),
        (0, 0),
        (32, 32),
    ],
)
@parametrize(
    "buybox_type, price_override, expected_price, expected_offer",
    [
        (BuyboxType.CUSTOM_1, None, 3002, 4444),
        (BuyboxType.CUSTOM_1, 8866, 8866, 4444),
        (BuyboxType.LOWEST_PRICED, None, 3001, 5555),
        (BuyboxType.LOWEST_PRICED, 8866, 8866, 5555),
        (BuyboxType.FASTEST, None, 3003, 3333),
        (BuyboxType.FASTEST, 8866, 8866, 3333),
    ],
)
def test_build_enhanced_ecommerce_add_to_cart(
    productline_one_variant,
    buybox_type,
    price_override,
    expected_price,
    expected_offer,
    quantity,
    expected_quantity,
):
    factory = DetailViewFactory(
        platform=Platform.WEB,
        buybox_type=buybox_type,
        productline=productline_one_variant,
    )

    kwargs = {}
    if quantity is not ...:
        kwargs["quantity"] = quantity

    output = factory.build_enhanced_ecommerce_add_to_cart(
        category_path=None, price_override=price_override, **kwargs
    )

    assert output.to_dict() == {
        "event": "addToCart",
        "ecommerce": {
            "currencyCode": "ZAR",
            "add": {
                "products": [
                    {
                        "id": "PLID1111",
                        "name": "Productline Title 1111",
                        "brand": "Summarisor",
                        "category": "",
                        "variant": None,
                        "dimension1": None,
                        "dimension2": expected_offer,
                        "price": expected_price,
                        "quantity": expected_quantity,
                        "position": 0,
                    }
                ]
            },
        },
    }
