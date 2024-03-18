import pytest
from pytest_cases import fixture, parametrize
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition

from storefront_api_views_product.errors import ViewConfigurationError
from storefront_api_views_product.views.enhanced_ecommerce import (
    EcommerceActionField,
    EnhancedEcommerceAddToCartViewFactory,
    EnhancedEcommerceClickViewFactory,
    EnhancedEcommerceImpression,
    EnhancedEcommerceImpressionViewFactory,
    EnhancedEcommerceListName,
)


@fixture()
def macbook_productline(macbook_productline_source):
    return AdaptersFactory.from_productline_lineage(macbook_productline_source)


@fixture()
def productline_size_variance(productline_source_size_variance):
    return AdaptersFactory.from_productline_lineage(productline_source_size_variance)


@fixture()
def macbook_productline_no_prices():
    return AdaptersFactory.from_productline_lineage(
        {
            "productline": {"id": 91107319},
            "variants": {
                "91245030": {
                    "variant": {
                        "id": 91245030,
                        "availability": {"reason": "", "status": "disabled"},
                        "selectors": {"colour": "Red"},
                    },
                    "offers": {
                        "202151368": {
                            "id": 202151368,
                            "availability": {
                                "reason": "Stock on hand",
                                "status": "buyable",
                            },
                            "condition": "new",
                        },
                    },
                },
                "91245031": {
                    "variant": {
                        "id": 91245031,
                        "availability": {"reason": "", "status": "disabled"},
                        "selectors": {"colour": "Green"},
                    },
                    "offers": {
                        "202151369": {
                            "id": 202151369,
                            "availability": {
                                "reason": "Stock on hand",
                                "status": "buyable",
                            },
                            "condition": "new",
                        },
                    },
                },
            },
        }
    )


@parametrize(
    "platform, buybox_type, expected_price",
    [
        (Platform.APP, BuyboxType.CUSTOM_1, 30569),
        (Platform.WEB, BuyboxType.CUSTOM_1, 31569),
    ],
)
def test_enhanced_ecommerce_add_to_cart_view_factory(
    macbook_productline, platform, buybox_type, expected_price
):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )

    factory = EnhancedEcommerceAddToCartViewFactory(
        buybox_type=buybox_type,
        enabled_variants=variants,
        offer=None,
        platform=platform,
    )

    category_path = ["A", "b", "c", "d", "e"]

    output = factory.build(
        category_path=category_path,
        position=11,
    )

    assert output.to_dict() == {
        "ecommerce": {
            "add": {
                "products": [
                    {
                        "brand": "Apple",
                        "category": "A/b/c/d/e",
                        "dimension1": None,
                        "dimension2": None,
                        "id": "PLID91107319",
                        "name": "Apple MacBook Pro 13inch M2 chip "
                        "with 8-core CPU and 10-core GPU "
                        "512GB SSD",
                        "position": 11,
                        "price": expected_price,
                        "quantity": 1,
                        "variant": None,
                    }
                ]
            },
            "currencyCode": "ZAR",
        },
        "event": "eec.addToCart",
    }


@parametrize(
    "platform, buybox_type, expected_price",
    [
        (Platform.APP, BuyboxType.CUSTOM_1, 30569),
        (Platform.WEB, BuyboxType.CUSTOM_1, 31569),
    ],
)
def test_enhanced_ecommerce_click_view_factory(
    macbook_productline, platform, buybox_type, expected_price
):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )

    factory = EnhancedEcommerceClickViewFactory(
        buybox_type=buybox_type,
        enabled_variants=variants,
        offer=None,
        platform=platform,
    )

    category_path = ["A", "b", "c", "d", "e"]

    output = factory.build(
        list_name=EnhancedEcommerceListName.DAILY_DEALS,
        category_path=category_path,
        position=166,
    )

    assert output.to_dict() == {
        "ecommerce": {
            "click": {
                "actionField": {"action": "click", "list": "Daily Deals"},
                "products": [
                    {
                        "brand": "Apple",
                        "category": "A/b/c/d/e",
                        "dimension1": None,
                        "dimension2": None,
                        "id": "PLID91107319",
                        "name": "Apple MacBook Pro 13inch M2 chip "
                        "with 8-core CPU and 10-core GPU "
                        "512GB SSD",
                        "position": 166,
                        "price": expected_price,
                        "quantity": 1,
                        "variant": None,
                    }
                ],
            }
        },
        "event": "eec.productClick",
    }


@parametrize(
    "platform, buybox_type, expected_price",
    [
        (Platform.APP, BuyboxType.CUSTOM_1, 30569),
        (Platform.WEB, BuyboxType.CUSTOM_1, 31569),
    ],
)
def test_enhanced_ecommerce_impression_view_factory(
    macbook_productline, platform, buybox_type, expected_price
):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )

    factory = EnhancedEcommerceImpressionViewFactory(
        buybox_type=buybox_type,
        enabled_variants=variants,
        offer=None,
        platform=platform,
    )

    category_path = ["A", "b", "c", "d", "e"]

    output = factory.build(
        list_name=EnhancedEcommerceListName.ON_TAB,
        category_path=category_path,
        position=241,
    )

    assert output.to_dict() == {
        "ecommerce": {
            "impressions": [
                {
                    "brand": "Apple",
                    "category": "A/b/c/d/e",
                    "dimension1": None,
                    "dimension2": None,
                    "id": "PLID91107319",
                    "list": "On-tab Promos",
                    "name": (
                        "Apple MacBook Pro 13inch M2 chip with 8-core CPU and "
                        "10-core GPU 512GB SSD"
                    ),
                    "position": 241,
                    "price": expected_price,
                    "variant": None,
                }
            ],
            "currencyCode": "ZAR",
        },
        "event": "eec.productImpressions",
    }


def test_enhanced_ecommerce_impression_drop_none_list():
    impression = EnhancedEcommerceImpression(
        plid="aaa",
        name="qq ww",
        list_name=None,
        brand=None,
        category="",
        variant=None,
        dimension1=None,
        dimension2=None,
        price=123,
        position=21,
    )

    output = impression.to_dict()

    assert output == {
        "id": "aaa",
        "name": "qq ww",
        "brand": None,
        "category": "",
        "variant": None,
        "dimension1": None,
        "dimension2": None,
        "price": 123,
        "position": 21,
    }


def test_enhanced_ecommerce_action_field_drop_none_list():
    impression = EcommerceActionField(list_name=None, action="act")

    output = impression.to_dict()

    assert output == {
        "action": "act",
    }


@parametrize(
    "position_offset, expected_positions",
    [
        (None, [0, 0]),
        (44, [44, 45]),
    ],
)
def test_enhanced_ecommerce_add_to_cart_view_merge_list(
    macbook_productline, position_offset, expected_positions
):
    platform = Platform.WEB

    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )

    # Build an offer from each variant as a standalone item
    items = []
    offers = variants.get_winning_offers(
        platform=platform,
        buybox_type=BuyboxType.CUSTOM_1,
        buybox_condition=OfferCondition.NEW,
    )
    for offer in offers:
        factory = EnhancedEcommerceAddToCartViewFactory(
            enabled_variants=None,
            buybox_type=BuyboxType.CUSTOM_1,
            offer=offer,
            platform=platform,
        )

        item = factory.build(category_path=["a", "b", str(offer.offer_id)], position=0)
        items.append(item)

    output = EnhancedEcommerceAddToCartViewFactory.merge_list(
        views=items, position_offset=position_offset
    )

    assert output.to_dict() == {
        "event": "eec.addToCart",
        "ecommerce": {
            "currencyCode": "ZAR",
            "add": {
                "products": [
                    {
                        "id": "PLID91107319",
                        "name": (
                            "Apple MacBook Pro 13inch M2 chip with 8-core CPU "
                            "and 10-core GPU 512GB SSD"
                        ),
                        "brand": "Apple",
                        "category": "a/b/202151368",
                        "variant": "Space Grey",
                        "dimension1": None,
                        "dimension2": 202151368,
                        "price": 30499,
                        "quantity": 1,
                        "position": expected_positions[0],
                    },
                    {
                        "id": "PLID91107319",
                        "name": (
                            "Apple MacBook Pro 13inch M2 chip with 8-core CPU "
                            "and 10-core GPU 512GB SSD"
                        ),
                        "brand": "Apple",
                        "category": "a/b/202151369",
                        "variant": "Silver",
                        "dimension1": None,
                        "dimension2": 202151369,
                        "price": 31569,
                        "quantity": 1,
                        "position": expected_positions[1],
                    },
                ]
            },
        },
    }


@parametrize(
    "position_offset, expected_positions",
    [
        (None, [0, 0]),
        (44, [44, 45]),
    ],
)
def test_enhanced_ecommerce_impression_view_merge_list(
    macbook_productline, position_offset, expected_positions
):
    platform = Platform.WEB

    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )

    # Build an offer from each variant as a standalone item
    items = []
    offers = variants.get_winning_offers(
        platform=platform,
        buybox_type=BuyboxType.CUSTOM_1,
        buybox_condition=OfferCondition.NEW,
    )
    for offer in offers:
        factory = EnhancedEcommerceImpressionViewFactory(
            enabled_variants=None,
            buybox_type=BuyboxType.CUSTOM_1,
            offer=offer,
            platform=platform,
        )

        item = factory.build(
            list_name=EnhancedEcommerceListName.CART_RECOMMENDATIONS,
            category_path=["a", "b", str(offer.offer_id)],
            position=0,
        )
        items.append(item)

    output = EnhancedEcommerceImpressionViewFactory.merge_list(
        views=items, position_offset=position_offset
    )

    assert output.to_dict() == {
        "event": "eec.productImpressions",
        "ecommerce": {
            "currencyCode": "ZAR",
            "impressions": [
                {
                    "id": "PLID91107319",
                    "name": (
                        "Apple MacBook Pro 13inch M2 chip with 8-core CPU "
                        "and 10-core GPU 512GB SSD"
                    ),
                    "brand": "Apple",
                    "category": "a/b/202151368",
                    "variant": "Space Grey",
                    "dimension1": None,
                    "dimension2": 202151368,
                    "price": 30499,
                    "position": expected_positions[0],
                    "list": "Cart Recommendations",
                },
                {
                    "id": "PLID91107319",
                    "name": (
                        "Apple MacBook Pro 13inch M2 chip with 8-core CPU "
                        "and 10-core GPU 512GB SSD"
                    ),
                    "brand": "Apple",
                    "category": "a/b/202151369",
                    "variant": "Silver",
                    "dimension1": None,
                    "dimension2": 202151369,
                    "price": 31569,
                    "position": expected_positions[1],
                    "list": "Cart Recommendations",
                },
            ],
        },
    }


def test_enhanced_ecommerce_base_factory_bad_parameters():
    with pytest.raises(ViewConfigurationError):
        EnhancedEcommerceAddToCartViewFactory(
            enabled_variants=None,
            buybox_type=BuyboxType.CUSTOM_1,
            offer=None,
            platform=Platform.WEB,
        )


def test_enhanced_ecommerce_base_factory_bad_pricing(macbook_productline):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants.variants.clear()

    factory = EnhancedEcommerceAddToCartViewFactory(
        enabled_variants=variants,
        buybox_type=BuyboxType.CUSTOM_1,
        offer=None,
        platform=Platform.WEB,
    )

    output = factory._get_price_range()

    assert output.min == 0
    assert output.max == 0
