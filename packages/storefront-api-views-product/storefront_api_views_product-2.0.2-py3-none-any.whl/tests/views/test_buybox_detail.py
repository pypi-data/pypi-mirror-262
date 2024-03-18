from dataclasses import dataclass

import pytest
from freezegun import freeze_time
from pytest_cases import fixture, fixture_ref, parametrize, parametrize_with_cases
from storefront_product_adapter.facades.pricing import PricingFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition

from storefront_api_views_product.errors import InvalidDataError
from storefront_api_views_product.views.buybox import (
    BuyboxDetailItem,
    BuyboxDetailViewFactory,
    BuyboxOfferDetail,
    DeliveryCharges,
)
from storefront_api_views_product.views.models import BaseViewModel

pytestmark = pytest.mark.views


@fixture
def macbook_variants(macbook_productline):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )
    return variants


@fixture
def macbook_variants_preorder(macbook_productline_preorder):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_preorder
    )
    return variants.filter_by_ids([91245031])


@fixture
def macbook_variants_out_of_stock_variant(macbook_productline_out_of_stock):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_out_of_stock
    )
    return variants.filter_by_ids([91245030])


@fixture
def macbook_variants_disabled(macbook_productline_disabled):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_disabled
    )
    return variants


@fixture
def macbook_variants_single_a(macbook_productline):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    return variants.filter_by_ids([91245031])


@fixture
def macbook_variants_single_b(macbook_productline):
    variants = CollectionsFactory.variants_from_productline_adapter(macbook_productline)
    return variants.filter_by_ids([91245030])


@fixture
def macbook_variants_low_promo(macbook_productline_promotion_less_than_twenty):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_promotion_less_than_twenty
    )
    return variants.filter_by_ids([91245030])


@fixture
def macbook_variants_high_promo(macbook_productline_promotion_more_than_twenty):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_promotion_more_than_twenty
    )
    return variants.filter_by_ids([91245030])


@fixture
def macbook_variants_mutlibuy_one(macbook_productline_multibuy_one):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_multibuy_one
    )
    return variants.filter_by_ids([91245030])


@fixture
def macbook_variants_mutlibuy_many(macbook_productline_multibuy_many):
    variants = CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_multibuy_many
    )
    return variants.filter_by_ids([91245030])


class TestBuildCases:
    """
    Return:
        variants
        platform
        buybox_type
        free_shipping_threshold
        heavy_charge
        winning_offers
        expected
    """

    _icon_fastest = "https://static.takealot.com/images/buybox-icons/fastest.png"
    _icon_lowest_priced = (
        "https://static.takealot.com/images/buybox-icons/lowest_priced.png"
    )

    @parametrize(
        "buybox_type, min_price",
        [
            (BuyboxType.LOWEST_PRICED, 30499),
            (BuyboxType.FASTEST, 30499),
        ],
    )
    def case_simple_summary(self, macbook_variants, buybox_type, min_price):
        expected = {
            "plid": 91107319,
            "buybox_items_type": "summary",
            "is_digital": False,
            "items": [
                {
                    "is_selected": True,
                    "is_preorder": False,
                    "is_add_to_cart_available": False,
                    "is_add_to_wishlist_available": False,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "offer_detail": {},
                    "price": min_price,
                    "pretty_price": f"From R {min_price:,}",
                    "add_to_cart_text": "Add to Cart",
                }
            ],
            "variants_call_to_action": "Select an option",
        }
        return (
            macbook_variants,
            Platform.WEB,
            buybox_type,
            123,
            None,
            {},
            expected,
        )

    def case_out_of_stock(self, macbook_variants_out_of_stock_variant):
        expected = {
            "plid": 91107319,
            "tsin": 91245030,
            "buybox_items_type": "single",
            "is_digital": False,
            "items": [
                {
                    "is_selected": True,
                    "is_preorder": False,
                    "is_add_to_cart_available": False,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": False,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "offer_detail": {},
                    "price": 1,
                    "pretty_price": "R 1",
                    "add_to_cart_text": "Add to Cart",
                }
            ],
        }
        return (
            macbook_variants_out_of_stock_variant,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {},
            expected,
        )

    def case_all_disabled(self, macbook_variants_disabled):
        # Yes there is `variants_call_to_action` on this level. Via the detail view
        # factory there would not be.
        expected = {
            "plid": 91107319,
            "buybox_items_type": "summary",
            "is_digital": False,
            "variants_call_to_action": "Select an option",
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
        return (
            macbook_variants_disabled,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {},
            expected,
        )

    def case_simple_single_a_cheap(self, macbook_variants_single_a):
        expected = {
            "plid": 91107319,
            "tsin": 91245031,
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
                    "price": 31569,
                    "listing_price": 31999,
                    "pretty_price": f"R {31569:,}",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151369,
                    "sponsored_ads_seller_id": "R513",
                }
            ],
        }
        offer = macbook_variants_single_a.variants[91245031].offers[202151369]
        return (
            macbook_variants_single_a,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {BuyboxType.LOWEST_PRICED: offer},
            expected,
        )

    def case_simple_single_a_fast(self, macbook_variants_single_a):
        expected = {
            "plid": 91107319,
            "tsin": 91245031,
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
                    "price": 31569,
                    "listing_price": 31999,
                    "pretty_price": f"R {31569:,}",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Fastest Delivery",
                        "preference": "fastest",
                        "icon_url": self._icon_fastest,
                    },
                    "sku": 202151369,
                    "sponsored_ads_seller_id": "R513",
                }
            ],
        }
        offer = macbook_variants_single_a.variants[91245031].offers[202151369]
        return (
            macbook_variants_single_a,
            Platform.WEB,
            BuyboxType.FASTEST,
            123,
            None,
            {BuyboxType.FASTEST: offer},
            expected,
        )

    def case_simple_single_b_cheap(self, macbook_variants_high_promo):
        expected = {
            "plid": 91107319,
            "tsin": 91245030,
            "buybox_items_type": "multi",
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
                    "price": 30499,
                    "listing_price": 31999,
                    "pretty_price": "R 30,499",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151368,
                    "sponsored_ads_seller_id": "R513",
                },
                {
                    "is_selected": False,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 30555,
                    "listing_price": 31888,
                    "pretty_price": "R 30,555",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Fastest Delivery",
                        "preference": "fastest",
                        "icon_url": self._icon_fastest,
                    },
                    "sku": 22222222,
                    "sponsored_ads_seller_id": "M555",
                },
            ],
        }
        offer_1 = macbook_variants_high_promo.variants[91245030].offers[202151368]
        offer_2 = macbook_variants_high_promo.variants[91245030].offers[22222222]
        return (
            macbook_variants_high_promo,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {
                BuyboxType.LOWEST_PRICED: offer_1,
                BuyboxType.FASTEST: offer_2,
            },
            expected,
        )

    def case_simple_single_b_fast(self, macbook_variants_single_b):
        expected = {
            "plid": 91107319,
            "tsin": 91245030,
            "buybox_items_type": "multi",
            "is_digital": False,
            "items": [
                {
                    "is_selected": False,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 30499,
                    "listing_price": 31999,
                    "pretty_price": "R 30,499",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151368,
                    "sponsored_ads_seller_id": "R513",
                },
                {
                    "is_selected": True,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 30555,
                    "listing_price": 31888,
                    "pretty_price": "R 30,555",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Fastest Delivery",
                        "preference": "fastest",
                        "icon_url": self._icon_fastest,
                    },
                    "sku": 22222222,
                    "sponsored_ads_seller_id": "M555",
                },
            ],
        }
        offer_1 = macbook_variants_single_b.variants[91245030].offers[202151368]
        offer_2 = macbook_variants_single_b.variants[91245030].offers[22222222]
        return (
            macbook_variants_single_b,
            Platform.WEB,
            BuyboxType.FASTEST,
            123,
            None,
            {
                BuyboxType.LOWEST_PRICED: offer_1,
                BuyboxType.FASTEST: offer_2,
            },
            expected,
        )

    def case_preorder(self, macbook_variants_preorder):
        expected = {
            "plid": 91107319,
            "tsin": 91245031,
            "buybox_items_type": "single",
            "is_digital": False,
            "items": [
                {
                    "is_selected": True,
                    "is_preorder": True,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 31569,
                    "listing_price": 31999,
                    "pretty_price": f"R {31569:,}",
                    "add_to_cart_text": "Pre-order",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151369,
                    "sponsored_ads_seller_id": "R513",
                }
            ],
        }
        offer = macbook_variants_preorder.variants[91245031].offers[202151369]
        return (
            macbook_variants_preorder,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {BuyboxType.LOWEST_PRICED: offer},
            expected,
        )

    def case_low_promo_web(self, macbook_variants_low_promo):
        expected = {
            "plid": 91107319,
            "tsin": 91245030,
            "buybox_items_type": "multi",
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
                    "price": 30499,
                    "listing_price": 31999,
                    "pretty_price": "R 30,499",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151368,
                    "sponsored_ads_seller_id": "R513",
                    "promotion_qty": 16,
                    "promotion_qty_display_text": "Only 16 left",
                },
                {
                    "is_selected": False,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 30555,
                    "listing_price": 31888,
                    "pretty_price": "R 30,555",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Fastest Delivery",
                        "preference": "fastest",
                        "icon_url": self._icon_fastest,
                    },
                    "sku": 22222222,
                    "sponsored_ads_seller_id": "M555",
                },
            ],
        }
        offer_1 = macbook_variants_low_promo.variants[91245030].offers[202151368]
        offer_2 = macbook_variants_low_promo.variants[91245030].offers[22222222]
        return (
            macbook_variants_low_promo,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {
                BuyboxType.LOWEST_PRICED: offer_1,
                BuyboxType.FASTEST: offer_2,
            },
            expected,
        )

    def case_low_promo_app(self, macbook_variants_low_promo):
        expected = {
            "plid": 91107319,
            "tsin": 91245030,
            "buybox_items_type": "multi",
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
                    "price": 30359,
                    "listing_price": 31999,
                    "pretty_price": "R 30,359",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151368,
                    "sponsored_ads_seller_id": "R513",
                },
                {
                    "is_selected": False,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 30333,
                    "listing_price": 31888,
                    "pretty_price": "R 30,333",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Fastest Delivery",
                        "preference": "fastest",
                        "icon_url": self._icon_fastest,
                    },
                    "sku": 22222222,
                    "sponsored_ads_seller_id": "M555",
                },
            ],
        }
        offer_1 = macbook_variants_low_promo.variants[91245030].offers[202151368]
        offer_2 = macbook_variants_low_promo.variants[91245030].offers[22222222]
        return (
            macbook_variants_low_promo,
            Platform.APP,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {
                BuyboxType.LOWEST_PRICED: offer_1,
                BuyboxType.FASTEST: offer_2,
            },
            expected,
        )

    @parametrize(
        "variants, multibuy_label, bundle_label",
        [
            (
                fixture_ref("macbook_variants_mutlibuy_one"),
                "Early Access Tech & Appliances",
                "Early Access Tech & Appliances",
            ),
            (
                fixture_ref("macbook_variants_mutlibuy_many"),
                "Save with Bundle Deals",
                "Save with Bundle Deals (2)",
            ),
        ],
    )
    def case_multibuy_one(self, variants, multibuy_label, bundle_label):
        expected = {
            "plid": 91107319,
            "tsin": 91245030,
            "buybox_items_type": "multi",
            "is_digital": False,
            "items": [
                {
                    "is_selected": True,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": True,
                    "multibuy_label": multibuy_label,
                    "bundle_label": bundle_label,
                    "delivery_charges": {},
                    "price": 30499,
                    "listing_price": 31999,
                    "pretty_price": "R 30,499",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Best Price",
                        "preference": "lowest_priced",
                        "icon_url": self._icon_lowest_priced,
                    },
                    "sku": 202151368,
                    "sponsored_ads_seller_id": "R513",
                    "promotion_qty": 16,
                    "promotion_qty_display_text": "Only 16 left",
                },
                {
                    "is_selected": False,
                    "is_preorder": False,
                    "is_add_to_cart_available": True,
                    "is_add_to_wishlist_available": True,
                    "is_free_shipping_available": True,
                    "multibuy_display": False,
                    "delivery_charges": {},
                    "price": 30555,
                    "listing_price": 31888,
                    "pretty_price": "R 30,555",
                    "add_to_cart_text": "Add to Cart",
                    "offer_detail": {
                        "display_text": "Fastest Delivery",
                        "preference": "fastest",
                        "icon_url": self._icon_fastest,
                    },
                    "sku": 22222222,
                    "sponsored_ads_seller_id": "M555",
                },
            ],
        }
        offer_1 = variants.variants[91245030].offers[202151368]
        offer_2 = variants.variants[91245030].offers[22222222]
        return (
            variants,
            Platform.WEB,
            BuyboxType.LOWEST_PRICED,
            123,
            None,
            {
                BuyboxType.LOWEST_PRICED: offer_1,
                BuyboxType.FASTEST: offer_2,
            },
            expected,
        )


# =====================================================================================
# =====================================================================================


def test_buybox_detail_item_to_dict_externals():
    @dataclass
    class TestView(BaseViewModel):
        a: int

        def to_dict(self):
            return {"a": self.a}

    item = BuyboxDetailItem(
        is_selected=True,
        is_preorder=True,
        is_add_to_cart_available=True,
        is_add_to_wishlist_available=True,
        is_free_shipping_available=True,
        multibuy_display=True,
        delivery_charges=DeliveryCharges(),
        offer_detail=BuyboxOfferDetail(
            display_text=None, preference=None, icon_url="icon"
        ),
        sku=1,
        price=2,
        pretty_price="3",
        listing_price=4,
        add_to_cart_text="5",
        multibuy_label="6",
        bundle_label="7",
        promotion_qty=8,
        promotion_qty_display_text="9",
        sponsored_ads_seller_id="10",
        loyalty_prices=[TestView(a=11), TestView(a=12)],
        credit_options_summary=TestView(a=13),
        stock_availability=TestView(a=14),
    )

    output = item.to_dict()

    assert output == {
        "is_selected": True,
        "is_preorder": True,
        "is_add_to_cart_available": True,
        "is_add_to_wishlist_available": True,
        "is_free_shipping_available": True,
        "multibuy_display": True,
        "delivery_charges": {},
        "offer_detail": {"icon_url": "icon"},
        "sku": 1,
        "price": 2,
        "pretty_price": "3",
        "listing_price": 4,
        "add_to_cart_text": "5",
        "multibuy_label": "6",
        "bundle_label": "7",
        "promotion_qty": 8,
        "promotion_qty_display_text": "9",
        "sponsored_ads_seller_id": "10",
        "loyalty_prices": [{"a": 11}, {"a": 12}],
        "credit_options_summary": {"a": 13},
        "stock_availability": {"a": 14},
    }


@parametrize_with_cases(
    [
        "variants",
        "platform",
        "buybox_type",
        "free_shipping_threshold",
        "heavy_charge",
        "winning_offers",
        "expected",
    ],
    cases=TestBuildCases,
)
@freeze_time("2021-11-23T13:00:00+00:00")
def test_build(
    mocker,
    variants,
    platform,
    buybox_type,
    free_shipping_threshold,
    heavy_charge,
    winning_offers,
    expected,
):
    pricing_collections = CollectionsFactory.pricing_from_variants(
        variants=variants,
        platform=platform,
        buybox_type=buybox_type,
        buybox_conditions_precedence=[
            OfferCondition.NEW,
            OfferCondition.USED,
        ],
    )

    factory = BuyboxDetailViewFactory(
        platform=platform,
        buybox_type=buybox_type,
        variants=variants,
        winning_offers=winning_offers,
        heavy_charge=heavy_charge,
        pricing=PricingFacade(collections=pricing_collections),
        free_shipping_threshold=free_shipping_threshold,
    )

    output = factory.build()

    assert output.to_dict() == expected


def test_build_offer_item_bad_availability(
    mocker, macbook_variants_out_of_stock_variant
):
    """
    Test the safety net for trying to build an offer item that is not buyable
    """
    factory = BuyboxDetailViewFactory(
        platform=Platform.WEB,
        buybox_type=BuyboxType.LOWEST_PRICED,
        variants=macbook_variants_out_of_stock_variant,
        winning_offers=mocker.Mock(),
        heavy_charge=200,
        pricing=mocker.Mock(),
        free_shipping_threshold=111,
    )

    offer = next(
        iter(macbook_variants_out_of_stock_variant.variants[91245030].offers.values())
    )

    with pytest.raises(InvalidDataError):
        factory._build_offer_item(offer=offer, buybox_type=mocker.Mock())


def test_build_offer_item_bad_price(mocker, macbook_variants_single_a):
    """
    Test the other safety net
    """
    factory = BuyboxDetailViewFactory(
        platform=Platform.WEB,
        buybox_type=BuyboxType.LOWEST_PRICED,
        variants=macbook_variants_single_a,
        winning_offers=mocker.Mock(),
        heavy_charge=200,
        pricing=mocker.Mock(),
        free_shipping_threshold=111,
    )

    offer = next(iter(macbook_variants_single_a.variants[91245031].offers.values()))
    mocker.patch.object(offer, "get_selling_price", return_value=None)

    with pytest.raises(InvalidDataError):
        factory._build_offer_item(offer=offer, buybox_type=mocker.Mock())


@parametrize(
    "is_digital, expected",
    [
        (True, False),
        (False, True),
    ],
)
def test_has_free_shipping(mocker, macbook_variants_single_a, is_digital, expected):
    pricing_collections = CollectionsFactory.pricing_from_variants(
        variants=macbook_variants_single_a,
        platform=Platform.WEB,
        buybox_type=BuyboxType.LOWEST_PRICED,
        buybox_conditions_precedence=[
            OfferCondition.NEW,
            OfferCondition.USED,
        ],
    )

    factory = BuyboxDetailViewFactory(
        platform=Platform.WEB,
        buybox_type=BuyboxType.LOWEST_PRICED,
        variants=macbook_variants_single_a,
        winning_offers=mocker.Mock(),
        heavy_charge=200,
        pricing=PricingFacade(collections=pricing_collections),
        free_shipping_threshold=111,
    )

    mocker.patch.object(
        macbook_variants_single_a.productline, "is_digital", return_value=is_digital
    )

    assert factory._has_free_shipping() == expected
