import json

import pytest
from storefront_product_adapter.adapters.productline import ProductlineAdapter
from storefront_product_adapter.models.reviews_summary import ReviewsSummary

from storefront_api_views_product.views.reviews import (
    ReviewsDistribution,
    ReviewsSummaryView,
    ReviewsSummaryViewFactory,
)

pytestmark = pytest.mark.views


def test_build(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = ReviewsSummaryViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(
        productline,
        "get_reviews_summary",
        return_value=ReviewsSummary(
            total=10,
            average_rating=4.5,
            ratings={
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
            },
        ),
    )

    output = view.build()

    assert output == ReviewsSummaryView(
        star_rating=4.5,
        review_count=10,
        distribution=ReviewsDistribution(
            num_1_star_ratings=1,
            num_2_star_ratings=2,
            num_3_star_ratings=3,
            num_4_star_ratings=4,
            num_5_star_ratings=5,
        ),
    )


def test_star_rating_rounds(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = ReviewsSummaryViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(
        productline,
        "get_reviews_summary",
        return_value=ReviewsSummary(
            total=10,
            average_rating=4.63201323232,
            ratings={
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
            },
        ),
    )

    output = view.build()

    assert output == ReviewsSummaryView(
        star_rating=4.6,
        review_count=10,
        distribution=ReviewsDistribution(
            num_1_star_ratings=1,
            num_2_star_ratings=2,
            num_3_star_ratings=3,
            num_4_star_ratings=4,
            num_5_star_ratings=5,
        ),
    )


def test_build_zero_reviews(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = ReviewsSummaryViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(
        productline,
        "get_reviews_summary",
        return_value=ReviewsSummary(
            total=0,
            average_rating=0,
            ratings={
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0,
                "5": 0,
            },
        ),
    )

    output = view.build()
    # We need to test that the output is indeed an int as python will interpret
    # 0.0 and 0 as the same thus rendering the test pointless
    assert isinstance(output.star_rating, int) and not output.star_rating


def test_build_no_reviews(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = ReviewsSummaryViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(productline, "get_reviews_summary", return_value=None)

    output = view.build()

    assert output == ReviewsSummaryView(
        star_rating=None, review_count=0, distribution=ReviewsDistribution()
    )


def test_view_to_dict():
    model = ReviewsSummaryView(
        star_rating=4.6,
        review_count=10,
        distribution=ReviewsDistribution(
            num_1_star_ratings=1,
            num_2_star_ratings=2,
            num_3_star_ratings=3,
            num_4_star_ratings=4,
            num_5_star_ratings=5,
        ),
    )
    output = model.to_dict()

    assert output == {
        "star_rating": 4.6,
        "review_count": 10,
        "distribution": {
            "num_1_star_ratings": 1,
            "num_2_star_ratings": 2,
            "num_3_star_ratings": 3,
            "num_4_star_ratings": 4,
            "num_5_star_ratings": 5,
        },
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict
