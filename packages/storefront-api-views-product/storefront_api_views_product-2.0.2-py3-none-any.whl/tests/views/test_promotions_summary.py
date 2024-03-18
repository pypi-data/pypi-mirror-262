import json

import pytest
from freezegun import freeze_time
from storefront_product_adapter.collections.variant import VariantCollection
from storefront_product_adapter.factories.adapters import AdaptersFactory

from storefront_api_views_product.views.promotions import (
    PromotionsSummaryView,
    PromotionsSummaryViewFactory,
)

pytestmark = pytest.mark.views


def test_build_no_variant(mocker):
    variants = VariantCollection(mocker.Mock)

    view = PromotionsSummaryViewFactory(buyable_variants=variants)
    output = view.build()
    assert output == PromotionsSummaryView(is_displayed=False, label=None)


def test_build_no_promotions(variant_doc_no_promotions):
    variant_adapter = AdaptersFactory.from_variant_lineage(
        catalogue_lineage_dict=variant_doc_no_promotions
    )
    variants = VariantCollection(variant_adapter.productline)
    variants.add(variant_adapter.variant_id, variant_adapter)

    view = PromotionsSummaryViewFactory(buyable_variants=variants)

    output = view.build()
    assert output == PromotionsSummaryView(is_displayed=False, label=None)


@freeze_time("2022-11-20T22:00:00+00:00")
def test_build_no_promo_filter(variant_doc):
    variant_adapter = AdaptersFactory.from_variant_lineage(
        catalogue_lineage_dict=variant_doc
    )
    variants = VariantCollection(variant_adapter.productline)
    variants.add(variant_adapter.variant_id, variant_adapter)

    view = PromotionsSummaryViewFactory(buyable_variants=variants)

    output = view.build()
    assert output == PromotionsSummaryView(
        is_displayed=True, label="Buy 4 Domestos for R140"
    )


@freeze_time("2022-11-20T22:00:00+00:00")
def test_build_no_promo_filter_empty_promo_ids(variant_doc):
    variant_adapter = AdaptersFactory.from_variant_lineage(
        catalogue_lineage_dict=variant_doc
    )
    variants = VariantCollection(variant_adapter.productline)
    variants.add(variant_adapter.variant_id, variant_adapter)

    view = PromotionsSummaryViewFactory(
        buyable_variants=variants, included_promotion_ids=[]
    )

    output = view.build()
    assert output == PromotionsSummaryView(
        is_displayed=True, label="Buy 4 Domestos for R140"
    )


@freeze_time("2022-11-20T22:00:00+00:00")
def test_build_promo_no_display_value(variant_doc_promotion_no_display_name):
    variant_adapter = AdaptersFactory.from_variant_lineage(
        catalogue_lineage_dict=variant_doc_promotion_no_display_name
    )
    variants = VariantCollection(variant_adapter.productline)
    variants.add(variant_adapter.variant_id, variant_adapter)

    view = PromotionsSummaryViewFactory(buyable_variants=variants)

    output = view.build()
    # How is this "True, None" and OK?
    assert output == PromotionsSummaryView(is_displayed=True, label=None)


@freeze_time("2022-11-20T22:00:00+00:00")
def test_build_filter_ids(variant_doc):
    variant_adapter = AdaptersFactory.from_variant_lineage(
        catalogue_lineage_dict=variant_doc
    )
    variants = VariantCollection(variant_adapter.productline)
    variants.add(variant_adapter.variant_id, variant_adapter)

    view = PromotionsSummaryViewFactory(
        buyable_variants=variants, included_promotion_ids=[76761]
    )

    output = view.build()
    assert output == PromotionsSummaryView(
        is_displayed=True, label="Buy 4 Domestos for R140"
    )


@freeze_time("2022-11-20T22:00:00+00:00")
def test_build_filter_ids_multiple_ids(variant_doc_multiple_promotions):
    variant_adapter = AdaptersFactory.from_variant_lineage(
        catalogue_lineage_dict=variant_doc_multiple_promotions
    )
    variants = VariantCollection(variant_adapter.productline)
    variants.add(variant_adapter.variant_id, variant_adapter)

    view = PromotionsSummaryViewFactory(
        buyable_variants=variants, included_promotion_ids=[76761, 75406]
    )

    output = view.build()
    assert output == PromotionsSummaryView(
        is_displayed=True, label="Save with Bundle Deals"
    )


def test_view_to_dict():
    model = PromotionsSummaryView(is_displayed=True, label="Test Label")
    output = model.to_dict()

    assert output == {"is_displayed": True, "label": "Test Label"}
    assert json.dumps(output)  # Ensure output is a JSON serializable dict
