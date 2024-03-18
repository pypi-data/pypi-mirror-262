import json

import pytest
from pytest_cases import fixture, parametrize
from storefront_product_adapter.collections import VariantCollection
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.stock import (
    LeadTimeRange,
    OfferStockStatus,
    StockQuantity,
)

from storefront_api_views_product.views.stock_availability import (
    DistributionCentre,
    InternalDistributionCentre,
    StockAvailabilitySummaryView,
    StockAvailabilitySummaryViewFactory,
)

pytestmark = pytest.mark.views


@fixture
def stock_availability_summary_only_cpt():
    return StockAvailabilitySummaryView(
        status="In stock",
        is_leadtime=False,
        is_imported=False,
        distribution_centres=[
            DistributionCentre(
                distribution_centre_id="distribution-centre-0",
                text="CPT",
                description="This item can be shipped from Cape Town.",
                info_mode="short",
            ),
        ],
        is_displayed=None,
    )


@fixture
def distribution_centres_from_stock():
    return [
        InternalDistributionCentre(
            text="BFN",
            description="This item can be shipped from BFN.",
            info_mode="short",
            long_name="BFN",
        ),
        InternalDistributionCentre(
            text="CPT",
            description="This item can be shipped from Cape Town.",
            info_mode="short",
            long_name="Cape Town",
        ),
        InternalDistributionCentre(
            text="JHB",
            description="This item can be shipped from Johannesburg.",
            info_mode="short",
            long_name="Johannesburg",
        ),
    ]


@parametrize(
    ["offer_status", "expected"],
    [
        (OfferStockStatus.PRE_ORDER_LIVE, "Pre-order: Ships 13 Jan, 2023"),
        (
            OfferStockStatus.OUT_OF_STOCK,
            "Supplier out of stock",
        ),
    ],
)
def test_get_availability_status_pre_order(mocker, offer_status, expected):
    mock_offer = mocker.Mock()
    mock_productline = mocker.Mock()

    mock_productline.timestamp_released = 1673616104
    mock_offer.variant.productline = mock_productline

    mock_offer.get_stock_status.return_value = offer_status

    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=mocker.Mock(),
        enabled_variants=None,
        specific_offer=mock_offer,
    )

    output = factory._get_availability_status(offer=mock_offer)

    assert output == (offer_status, expected)


@parametrize(
    ["lead_time_range", "expected"],
    [
        (LeadTimeRange(min_days=1, max_days=5), "Ships in 1 - 5 work days"),
        (LeadTimeRange(min_days=3, max_days=9), "Ships in 3 - 9 work days"),
    ],
)
def test_get_availability_status_lead_time(mocker, lead_time_range, expected):
    mock_offer = mocker.Mock()
    mock_offer.get_stock_status.return_value = OfferStockStatus.LEAD_TIME
    mock_offer.get_leadtimes.return_value = lead_time_range

    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=mocker.Mock(),
        enabled_variants=None,
        specific_offer=mock_offer,
    )

    output = factory._get_availability_status(offer=mock_offer)

    assert output == (OfferStockStatus.LEAD_TIME, expected)


@parametrize(
    ["unboxed_offer", "is_digital", "expected"],
    [
        (True, False, "Unboxed stock available"),
        (False, False, "In stock"),
        (False, True, "Available now"),
    ],
)
def test_get_availability_status_in_stock(mocker, unboxed_offer, is_digital, expected):
    mock_offer = mocker.Mock()
    mock_offer.get_stock_status.return_value = OfferStockStatus.IN_STOCK
    mock_offer.variant.productline.is_digital.return_value = is_digital
    mock_offer.is_unboxed_offer.return_value = unboxed_offer

    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=mocker.Mock(),
        enabled_variants=None,
        specific_offer=mock_offer,
    )

    output = factory._get_availability_status(offer=mock_offer)

    assert output == (OfferStockStatus.IN_STOCK, expected)


def test_build_distribution_centres(mocker, distribution_centres_from_stock):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=mocker.Mock(),
        enabled_variants=None,
        specific_offer=mocker.Mock(),
    )

    stock_quantities = StockQuantity(
        warehouse_regions={
            "cpt": 1,
            "jhb": 6,
            "dbn": 0,
            "bfn": 1,
        },
        warehouses_total=12,
        merchant=mocker.Mock(),
    )
    output = factory._build_distribution_centres(
        stock_qtys=stock_quantities,
    )

    assert output == distribution_centres_from_stock


@parametrize(
    "buybox_type",
    [BuyboxType.CUSTOM_1, BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST],
)
@parametrize(
    "displayed_in, displayed_expected",
    [(None, None), (False, False), (True, True)],
)
def test_build_out_of_stock_collection(
    macbook_variants_out_of_stock,
    buybox_type,
    displayed_in,
    displayed_expected,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=macbook_variants_out_of_stock,
        specific_offer=None,
    )

    output = factory.build(is_displayed=displayed_in)

    assert output == StockAvailabilitySummaryView(
        is_leadtime=False,
        is_imported=False,
        status="Supplier out of stock",
        distribution_centres=[],
        is_displayed=displayed_expected,
    )


@parametrize(
    "displayed_in, displayed_expected",
    [(None, None), (False, False), (True, False)],
)
def test_build_all_none(displayed_in, displayed_expected):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=BuyboxType.LOWEST_PRICED,
        enabled_variants=None,
        specific_offer=None,
    )

    output = factory.build(is_displayed=displayed_in)

    assert output == StockAvailabilitySummaryView(
        is_leadtime=False,
        is_imported=False,
        status="",
        distribution_centres=[],
        is_displayed=displayed_expected,
    )


@parametrize(
    "buybox_type",
    [BuyboxType.CUSTOM_1, BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST],
)
@parametrize(
    "displayed_in, displayed_expected",
    [(None, None), (False, False), (True, True)],
)
def test_build_out_of_stock_empty(
    mocker,
    buybox_type,
    displayed_in,
    displayed_expected,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=VariantCollection(productline=mocker.Mock()),
        specific_offer=None,
    )

    output = factory.build(is_displayed=displayed_in)

    assert output == StockAvailabilitySummaryView(
        is_leadtime=False,
        is_imported=False,
        status="Supplier out of stock",
        distribution_centres=[],
        is_displayed=displayed_expected,
    )


def test_build_has_offer(mocker, stock_availability_summary_only_cpt):
    mock_offer = mocker.Mock()
    mock_offer.variant.productline.is_white_good.return_value = False
    mock_offer.variant.productline.is_prepaid.return_value = False
    mock_offer.variant.productline.get_colour_selector_names.return_value = False
    mock_offer.variant.productline.get_size_selector_names.return_value = False
    mock_offer.variant.productline.is_digital.return_value = False
    mock_offer.is_unboxed_offer.return_value = False
    mock_offer.get_stock_status.return_value = OfferStockStatus.IN_STOCK
    mock_offer.get_stock_quantities.return_value = StockQuantity(
        warehouse_regions={
            "cpt": 1,
            "jhb": 0,
            "dbn": 0,
        },
        warehouses_total=12,
        merchant=mocker.Mock(),
    )

    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=BuyboxType.CUSTOM_1,
        enabled_variants=None,
        specific_offer=mock_offer,
    )

    output = factory.build(is_displayed=None)

    assert output == stock_availability_summary_only_cpt


@parametrize(
    "buybox_type, is_displayed, expected_displayed",
    [
        (BuyboxType.CUSTOM_1, None, None),
        (BuyboxType.CUSTOM_1, False, False),
        (BuyboxType.CUSTOM_1, True, False),
        (BuyboxType.LOWEST_PRICED, None, None),
        (BuyboxType.LOWEST_PRICED, False, False),
        (BuyboxType.LOWEST_PRICED, True, False),
    ],
)
def test_build_variants(
    macbook_variants,
    buybox_type,
    is_displayed,
    expected_displayed,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=macbook_variants,
        specific_offer=None,
    )

    output = factory.build(is_displayed=is_displayed)

    assert output.status == ""
    assert output.is_displayed == expected_displayed
    assert output.distribution_centres == []


@parametrize(
    "buybox_type, is_displayed, expected_status, expected_displayed, expected_dcs",
    [
        (BuyboxType.CUSTOM_1, None, "In stock", None, ["JHB"]),
        (BuyboxType.CUSTOM_1, False, "In stock", False, ["JHB"]),
        (BuyboxType.CUSTOM_1, True, "In stock", True, ["JHB"]),
        (BuyboxType.LOWEST_PRICED, None, "In stock", None, ["CPT"]),
        (BuyboxType.LOWEST_PRICED, False, "In stock", False, ["CPT"]),
        (BuyboxType.LOWEST_PRICED, True, "In stock", True, ["CPT"]),
    ],
)
def test_build_variants_single_winner(
    macbook_variants_single_variant_single_winner,
    buybox_type,
    is_displayed,
    expected_status,
    expected_displayed,
    expected_dcs,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=macbook_variants_single_variant_single_winner,
        specific_offer=None,
    )

    output = factory.build(is_displayed=is_displayed)

    assert output.status == expected_status
    assert output.is_displayed == expected_displayed
    assert [dc.text for dc in output.distribution_centres] == expected_dcs


@parametrize(
    "buybox_type, is_displayed, expected_status, expected_displayed",
    [
        (BuyboxType.CUSTOM_1, None, "In stock", None),
        (BuyboxType.CUSTOM_1, False, "In stock", False),
        (BuyboxType.CUSTOM_1, True, "In stock", True),
        (BuyboxType.LOWEST_PRICED, None, "", None),
        (BuyboxType.LOWEST_PRICED, False, "", False),
        (BuyboxType.LOWEST_PRICED, True, "", False),
    ],
)
def test_build_single_variant_multi_offer(
    macbook_variants_single_variant_multi_winner,
    buybox_type,
    is_displayed,
    expected_status,
    expected_displayed,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=macbook_variants_single_variant_multi_winner,
        specific_offer=None,
    )

    output = factory.build(is_displayed=is_displayed)

    assert output.status == expected_status
    assert output.is_displayed == expected_displayed


@parametrize(
    "buybox_type, is_displayed, expected_status, expected_displayed, expected_dcs",
    [
        (BuyboxType.CUSTOM_1, None, "", None, []),
        (BuyboxType.CUSTOM_1, False, "", False, []),
        (BuyboxType.CUSTOM_1, True, "", False, []),
        (BuyboxType.LOWEST_PRICED, None, "", None, []),
        (BuyboxType.LOWEST_PRICED, False, "", False, []),
        (BuyboxType.LOWEST_PRICED, True, "", False, []),
    ],
)
def test_build_variants_single_in_stock(
    macbook_variants_multi_variant_single_winner,
    buybox_type,
    is_displayed,
    expected_status,
    expected_displayed,
    expected_dcs,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=macbook_variants_multi_variant_single_winner,
        specific_offer=None,
    )

    output = factory.build(is_displayed=is_displayed)

    assert output.status == expected_status
    assert output.is_displayed == expected_displayed
    assert [dc.text for dc in output.distribution_centres] == expected_dcs


@parametrize(
    "buybox_type, is_displayed, expected_status, expected_displayed",
    [
        (BuyboxType.CUSTOM_1, None, "In stock", None),
        (BuyboxType.CUSTOM_1, False, "In stock", False),
        (BuyboxType.CUSTOM_1, True, "In stock", True),
        (BuyboxType.LOWEST_PRICED, None, "In stock", None),
        (BuyboxType.LOWEST_PRICED, False, "In stock", False),
        (BuyboxType.LOWEST_PRICED, True, "In stock", True),
    ],
)
def test_build_variants_no_regions(
    macbook_variants_single_variant_used_winner,
    buybox_type,
    is_displayed,
    expected_status,
    expected_displayed,
):
    factory = StockAvailabilitySummaryViewFactory(
        buybox_type=buybox_type,
        enabled_variants=macbook_variants_single_variant_used_winner,
        specific_offer=None,
    )

    output = factory.build(is_displayed=is_displayed)

    assert output.status == expected_status
    assert output.is_displayed == expected_displayed
    assert [dc.text for dc in output.distribution_centres] == ["CPT", "JHB"]


def test_stock_availability_summary_view_to_dict(mocker):
    stock_availability_summary_view = StockAvailabilitySummaryView(
        status="In stock",
        is_leadtime=False,
        is_imported=False,
        distribution_centres=[
            DistributionCentre(
                distribution_centre_id="distribution-centre-0",
                text="JHB",
                description="description",
                info_mode="short",
            ),
        ],
        is_displayed=None,
    )

    output = stock_availability_summary_view.to_dict()
    assert output == {
        "status": "In stock",
        "is_leadtime": False,
        "is_imported": False,
        "distribution_centres": [
            {
                "id": "distribution-centre-0",
                "text": "JHB",
                "info_mode": "short",
                "description": "description",
            }
        ],
    }

    assert json.dumps(output)


def test_stock_availability_summary_view_to_dict_offer_opt(mocker):
    stock_availability_summary_view = StockAvailabilitySummaryView(
        status="In stock",
        is_leadtime=False,
        is_imported=False,
        distribution_centres=[
            DistributionCentre(
                distribution_centre_id="distribution-centre-0",
                text="JHB",
                description="description",
                info_mode="short",
            ),
        ],
        is_displayed=False,
    )

    output = stock_availability_summary_view.to_dict()
    assert output == {
        "status": "In stock",
        "is_leadtime": False,
        "is_imported": False,
        "distribution_centres": [
            {
                "id": "distribution-centre-0",
                "text": "JHB",
                "info_mode": "short",
                "description": "description",
            }
        ],
        "is_displayed": False,
    }

    assert json.dumps(output)
