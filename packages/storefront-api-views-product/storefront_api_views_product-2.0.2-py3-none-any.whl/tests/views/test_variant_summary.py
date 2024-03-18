import json
from unittest.mock import Mock

import pytest
from pytest_cases import parametrize
from storefront_product_adapter.models.selectors import SelectorFilter, VariantSelectors

from storefront_api_views_product.views.variant import (
    AppliedSelector,
    VariantSummaryView,
    VariantSummaryViewFactory,
)

pytestmark = pytest.mark.views


@pytest.mark.parametrize(
    "selector_filter, expected",
    [
        (
            SelectorFilter(colour=["Red", "Blue"]),
            {"has_more_colours": True, "applied_selectors": []},
        ),
        (
            SelectorFilter(colour=["Red"]),
            {"has_more_colours": False, "applied_selectors": []},
        ),
        (
            SelectorFilter(colour=None),
            {"has_more_colours": False, "applied_selectors": []},
        ),
    ],
)
def test_variant_summary_has_more_colours(mocker, selector_filter, expected):

    mock_variants = mocker.Mock()
    mock_variants.is_empty.return_value = False
    mock_variants.get_selector_filter.return_value = selector_filter

    mock_variants.get_singular.return_value.get_applied_selector_names.return_value = (
        VariantSelectors(colour=None, size=None)
    )

    factory = VariantSummaryViewFactory(enabled_variants=mock_variants)

    output = factory.build()

    assert output.has_more_colours == expected["has_more_colours"]
    assert output.applied_selectors == expected["applied_selectors"]


@pytest.mark.parametrize(
    "input_variant_selectors, expected",
    [
        (
            VariantSelectors(colour="Red", size=None),
            {
                "has_more_colours": False,
                "applied_selectors": [
                    AppliedSelector(key="colour_variant", value="Red")
                ],
            },
        ),
        (
            VariantSelectors(colour=None, size="Large"),
            {
                "has_more_colours": False,
                "applied_selectors": [AppliedSelector(key="size", value="Large")],
            },
        ),
        (
            VariantSelectors(colour="Red", size="Large"),
            {
                "has_more_colours": False,
                "applied_selectors": [
                    AppliedSelector(key="colour_variant", value="Red"),
                    AppliedSelector(key="size", value="Large"),
                ],
            },
        ),
    ],
)
def test_variant_summary_applied_filters(input_variant_selectors, expected):
    mock_variants = Mock()

    mock_variants.get_singular.return_value.get_applied_selector_names.return_value = (
        input_variant_selectors
    )

    mock_variants.get_selector_filter.return_value = SelectorFilter()

    factory = VariantSummaryViewFactory(enabled_variants=mock_variants)

    output = factory.build()

    assert output.applied_selectors == expected["applied_selectors"]


def test_variant_summary_variant_collection_empty(mocker):
    mock_variants = mocker.Mock()
    mock_variants.is_empty.return_value = True

    mock_variants.get_singular.return_value = None

    view = VariantSummaryViewFactory(enabled_variants=mock_variants)

    output = view.build()

    assert output == VariantSummaryView(has_more_colours=False, applied_selectors=[])


@parametrize(
    ["model", "expected"],
    [
        (
            VariantSummaryView(has_more_colours=False, applied_selectors=[]),
            {"has_more_colours": False, "applied_selectors": []},
        ),
        (
            VariantSummaryView(has_more_colours=True, applied_selectors=[]),
            {"has_more_colours": True, "applied_selectors": []},
        ),
        (
            VariantSummaryView(
                has_more_colours=False,
                applied_selectors=[
                    AppliedSelector(key="colour_variant", value="Red"),
                    AppliedSelector(key="size", value="Large"),
                ],
            ),
            {
                "has_more_colours": False,
                "applied_selectors": [
                    {"key": "colour_variant", "value": "Red"},
                    {"key": "size", "value": "Large"},
                ],
            },
        ),
    ],
)
def test_view_to_dict(model, expected):
    output = model.to_dict()
    assert output == expected
    assert json.dumps(output)  # Ensure output is a JSON serializable dict
