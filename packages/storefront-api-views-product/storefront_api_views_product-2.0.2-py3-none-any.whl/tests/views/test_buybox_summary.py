import json

import pytest
from freezegun import freeze_time
from pytest_cases import parametrize_with_cases
from storefront_product_adapter.collections.variant import VariantCollection
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.buybox import BuyboxType

from storefront_api_views_product.views.buybox import (
    BuyboxSummaryView,
    BuyboxSummaryViewFactory,
    DeliveryCharges,
    HeavyCharge,
    InfoType,
)

pytestmark = pytest.mark.views


class TestBuildCases:
    """
    Cases for `test_build`
    Methods return productline, heavy_charge, expected, buybox_type
    """

    def case_multi_offer_same_price(self, productline_source_size_variance):
        productline = AdaptersFactory.from_productline_lineage(
            productline_source_size_variance
        )

        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="R 200",
            app_pretty_price="R 200",
            prices=[200],
            app_prices=[200],
            saving=None,
            app_saving=None,
            is_add_to_cart_available=False,
            is_shop_all_options_available=True,
            is_add_to_wish_list_available=False,
            product_id=333,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=222,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )

        return productline, None, expected, BuyboxType.LOWEST_PRICED

    def case_single_variant_multi_offer_different_price(
        self, macbook_productline_single_variant_multi_winner_source
    ):
        """
        Test OfferOpt enabled (via buybox_type) with single variant that has
        different buybox winners on Web only.

        |   Offer   | App price | Web price | custom_1 | lowest_priced | fastest  |
        |-----------|-----------|-----------|----------|---------------|----------|
        | 202151368 |     30359 |     30499 | web, app | web           |          |
        |  22222222 |     30333 |     30555 |          | app           | web, app |

        """
        productline = AdaptersFactory.from_productline_lineage(
            macbook_productline_single_variant_multi_winner_source
        )

        expected = BuyboxSummaryView(
            listing_price=None,  # Can't show list price with different winners
            pretty_price="From R 30,499",
            app_pretty_price="R 30,333",
            prices=[30499, 30555],
            app_prices=[30333],
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=False,
            is_shop_all_options_available=True,
            is_add_to_wish_list_available=True,
            product_id=22222222,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )

        return productline, None, expected, BuyboxType.LOWEST_PRICED

    def case_single_variant_multi_offer_custom_1(
        self, macbook_productline_single_variant_multi_winner_source
    ):
        """
        Test OfferOpt disabled (via buybox_type) with single variant.

        Productline level max price app+web = 31569
        """
        productline = AdaptersFactory.from_productline_lineage(
            macbook_productline_single_variant_multi_winner_source
        )

        expected = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 30,499",
            app_pretty_price="R 30,359",
            prices=[30499],
            app_prices=[30359],
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_shop_all_options_available=False,
            is_add_to_wish_list_available=True,
            product_id=202151368,  # Cheapest custom_1 app winner
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )

        return productline, None, expected, BuyboxType.CUSTOM_1

    def case_single_variant_used_offer_fastest(
        self, macbook_productline_single_variant_used_winner_source
    ):
        productline = AdaptersFactory.from_productline_lineage(
            macbook_productline_single_variant_used_winner_source
        )

        expected = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 21,569",
            app_pretty_price="R 20,569",
            prices=[21569],
            app_prices=[20569],
            saving=None,
            app_saving=None,
            is_add_to_cart_available=True,
            is_shop_all_options_available=False,
            is_add_to_wish_list_available=False,
            product_id=99202151369,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=9991245031,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )

        return productline, None, expected, BuyboxType.FASTEST

    def case_none_heavy_charge(self, macbook_productline):
        productline = macbook_productline

        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="From R 30,499",
            prices=[30499, 31569],
            app_prices=[30359, 30569],
            app_pretty_price="From R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=False,
            is_add_to_wish_list_available=False,
            is_shop_all_options_available=True,
            product_id=202151368,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return productline, None, expected, BuyboxType.CUSTOM_1

    def case_has_heavy_charge(self, heavy_charge_macbook_productline):
        productline = heavy_charge_macbook_productline

        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="From R 30,499",
            prices=[30499, 31569],
            app_prices=[30359, 30569],
            app_pretty_price="From R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=False,
            is_add_to_wish_list_available=False,
            is_shop_all_options_available=True,
            product_id=202151368,
            delivery_charges=DeliveryCharges(
                heavy_charge=HeavyCharge(
                    cost=200,
                    info="A R 200 heavy/bulky delivery surcharge applies to this item.",
                    text="+ R 200 Delivery Surcharge",
                    info_type=InfoType.SHORT,
                )
            ),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return productline, 200, expected, BuyboxType.CUSTOM_1

    def case_no_selling_price_difference(
        self, macbook_offer_no_listing_price_difference
    ):
        productline = macbook_offer_no_listing_price_difference.variant.productline

        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="R 31,990",
            prices=[31990],
            app_prices=[30359],
            app_pretty_price="R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=202151368,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return (
            productline,
            None,
            expected,
            BuyboxType.CUSTOM_1,
        )

    def case_productline_has_single_variant(
        self, macbook_productline_single_variant_multi_winner
    ):
        productline = macbook_productline_single_variant_multi_winner
        variants = CollectionsFactory.variants_from_productline_adapter(productline)
        assert len(variants) == 1  # Test assumption on input data
        variant = variants.get_singular()
        offers = CollectionsFactory.offers_from_variant_adapter(variant)
        assert len(offers) == 2  # Test assumption on input data

        expected = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 30,499",
            prices=[30499],
            app_prices=[30359],
            app_pretty_price="R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=202151368,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return (productline, None, expected, BuyboxType.CUSTOM_1)

    def case_promotion_has_more_than_twenty_available(
        self, macbook_productline_promotion_more_than_twenty
    ):
        productline = macbook_productline_promotion_more_than_twenty

        expected = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 30,499",
            prices=[30499],
            app_prices=[30359],
            app_pretty_price="R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=202151368,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return (productline, None, expected, BuyboxType.CUSTOM_1)

    def case_promotion_has_less_than_twenty_available(
        self, macbook_productline_promotion_less_than_twenty
    ):
        productline = macbook_productline_promotion_less_than_twenty

        expected = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 30,499",
            prices=[30499],
            app_prices=[30359],
            app_pretty_price="R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=202151368,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=16,
            promotion_qty_display_text="Only 16 left",
        )
        return (productline, None, expected, BuyboxType.CUSTOM_1)


class TestBuildOutOfStockCases:
    """
    Cases for `test_build_out_of_stock`
    Methods return productline, heavy_charge, expected
    """

    def case_variants(self, macbook_productline_out_of_stock):
        productline = macbook_productline_out_of_stock

        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="From R 1",
            prices=[1, 4],
            app_prices=[2, 3],
            app_pretty_price="From R 2",
            saving=None,
            app_saving=None,
            is_add_to_cart_available=False,
            is_add_to_wish_list_available=False,
            is_shop_all_options_available=False,
            product_id=None,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=None,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return productline, None, expected

    def case_single_variant(self, macbook_productline_single_variant_out_of_stock):
        productline = macbook_productline_single_variant_out_of_stock

        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="R 1",
            prices=[1],
            app_prices=[2],
            app_pretty_price="R 2",
            saving=None,
            app_saving=None,
            is_add_to_cart_available=False,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=None,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )
        return productline, None, expected


class TestBuildDisabledCases:
    """
    Cases for `test_build_disabled`
    Methods return variants,  heavy_charge, expected
    """

    def case_variants(self, macbook_productline_disabled):
        expected = BuyboxSummaryView(
            listing_price=None,
            pretty_price="",
            prices=[],
            app_prices=[],
            app_pretty_price="",
            saving=None,
            app_saving=None,
            is_add_to_cart_available=False,
            is_add_to_wish_list_available=False,
            is_shop_all_options_available=False,
            product_id=None,
            delivery_charges=DeliveryCharges(heavy_charge=None),
            tsin=None,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=None,
            promotion_qty_display_text=None,
        )

        return VariantCollection(macbook_productline_disabled), None, expected


# =====================================================================================
# =====================================================================================
@parametrize_with_cases(
    "productline, heavy_charge, expected, buybox_type", cases=TestBuildCases
)
@freeze_time("2021-11-23T13:00:00+00:00")
def test_build(mocker, productline, heavy_charge, expected, buybox_type):
    variants = CollectionsFactory.variants_from_productline_adapter(productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )
    factory = BuyboxSummaryViewFactory.from_variants(
        buybox_type=buybox_type,
        enabled_variants=variants,
        heavy_charge=heavy_charge,
    )

    assert factory.build() == expected


@parametrize_with_cases(
    "productline, heavy_charge, expected", cases=TestBuildOutOfStockCases
)
@freeze_time("2021-11-23T13:00:00+00:00")
def test_build_out_of_stock(mocker, productline, heavy_charge, expected):
    variants = CollectionsFactory.variants_from_productline_adapter(productline)
    variants = variants.filter_by_availability(
        [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
    )
    factory = BuyboxSummaryViewFactory.from_variants(
        buybox_type=BuyboxType.CUSTOM_1,
        enabled_variants=variants,
        heavy_charge=heavy_charge,
    )

    assert factory.build() == expected


@parametrize_with_cases(
    "variants, heavy_charge, expected", cases=TestBuildDisabledCases
)
@freeze_time("2021-11-23T13:00:00+00:00")
def test_build_disabled(mocker, variants, heavy_charge, expected):
    factory = BuyboxSummaryViewFactory.from_variants(
        buybox_type=BuyboxType.CUSTOM_1,
        enabled_variants=variants,
        heavy_charge=heavy_charge,
    )

    assert factory.build() == expected


# =====================================================================================
# =====================================================================================


class TestToDictCases:
    def case_has_heavy_charge(self):
        model = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 30,499",
            prices=[30499],
            app_prices=[30359],
            app_pretty_price="R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=91107319,
            delivery_charges=DeliveryCharges(
                heavy_charge=HeavyCharge(info="Foo", cost=200, text="Foo Bar")
            ),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=18,
            promotion_qty_display_text="Only 18 left",
        )

        expected = {
            "listing_price": 31999,
            "pretty_price": "R 30,499",
            "prices": [30499],
            "app_prices": [30359],
            "app_pretty_price": "R 30,359",
            "saving": "10%",
            "app_saving": "15%",
            "is_add_to_cart_available": True,
            "is_add_to_wish_list_available": True,
            "is_shop_all_options_available": False,
            "product_id": 91107319,
            "delivery_charges": {
                "heavy_charge": {
                    "info": "Foo",
                    "cost": 200,
                    "text": "Foo Bar",
                    "info_type": "short",
                }
            },
            "tsin": 91245030,
            "is_preorder": False,
            "add_to_cart_text": "Add to Cart",
            "promotion_qty": 18,
            "promotion_qty_display_text": "Only 18 left",
        }

        return model, expected

    def case_none_heavy_charge(self):
        model = BuyboxSummaryView(
            listing_price=31999,
            pretty_price="R 30,499",
            prices=[30499],
            app_prices=[30359],
            app_pretty_price="R 30,359",
            saving="10%",
            app_saving="15%",
            is_add_to_cart_available=True,
            is_add_to_wish_list_available=True,
            is_shop_all_options_available=False,
            product_id=91107319,
            delivery_charges=DeliveryCharges(),
            tsin=91245030,
            is_preorder=False,
            add_to_cart_text="Add to Cart",
            promotion_qty=18,
            promotion_qty_display_text="Only 18 left",
        )

        expected = {
            "listing_price": 31999,
            "pretty_price": "R 30,499",
            "prices": [30499],
            "app_prices": [30359],
            "app_pretty_price": "R 30,359",
            "saving": "10%",
            "app_saving": "15%",
            "is_add_to_cart_available": True,
            "is_add_to_wish_list_available": True,
            "is_shop_all_options_available": False,
            "product_id": 91107319,
            "delivery_charges": {},
            "tsin": 91245030,
            "is_preorder": False,
            "add_to_cart_text": "Add to Cart",
            "promotion_qty": 18,
            "promotion_qty_display_text": "Only 18 left",
        }

        return model, expected


@parametrize_with_cases("model, expected", cases=TestToDictCases)
def test_to_dict(model, expected):
    output = model.to_dict()
    assert output == expected
    assert json.dumps(output)  # Ensure output is a JSON serializable dict
