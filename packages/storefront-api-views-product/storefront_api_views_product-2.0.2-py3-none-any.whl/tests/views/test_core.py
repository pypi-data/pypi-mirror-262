import json

import pytest
from storefront_product_adapter.adapters import ProductlineAdapter, VariantAdapter
from storefront_product_adapter.models.attribute import Attribute
from storefront_product_adapter.models.reviews_summary import ReviewsSummary

from storefront_api_views_product.views.core import CoreView, CoreViewFactory
from storefront_api_views_product.views.models import (
    Author,
    BrandUrlLinkData,
    ContextualLinkData,
    Format,
    LinkData,
)

pytestmark = pytest.mark.views


@pytest.fixture
def reviews_summary():
    return ReviewsSummary(
        total=10,
        average_rating=4.5,
        ratings={"1": 1, "2": 2, "3": 3, "4": 4, "5": 5},
    )


@pytest.fixture
def authors():
    return [
        Author(
            author_id=-1,
            author="Test Author",
            link_data=LinkData(
                path="/all?filter=Author:{author_slug}",
                fields={"author_slug": "Test Author"},
            ),
        )
    ]


@pytest.fixture
def formats():
    return [
        Format(
            format_type_id=2,
            format_type="Green",
            name="Test name value green",
            format_id=321,
            link_data=ContextualLinkData(
                action="search",
                context="navigation",
                parameters={
                    "search": {
                        "filters": {
                            "Available": True,
                            "Format": "Test+name+value+green",
                        }
                    }
                },
            ),
        )
    ]


def test_build(mocker, reviews_summary, authors, formats):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(
        productline, "get_reviews_summary", return_value=reviews_summary
    )
    mocker.patch.object(view, "_get_authors", return_value=authors)
    mocker.patch.object(view, "_get_formats", return_value=formats)
    output = view.build()

    assert output == CoreView(
        productline_id=123,
        authors=authors,
        formats=formats,
        brand="Test Brand",
        brand_url=BrandUrlLinkData(
            link_data=LinkData(
                path="/all?filter=Brand:{brand_slug}",
                fields={"brand_slug": "Test+Brand"},
            )
        ),
        reviews=10,
        star_rating=4.5,
        slug="test-title",
        title="Test Title",
        subtitle="Test Subtitle",
    )


def test_build_with_selected_variant(mocker, reviews_summary, authors, formats):
    productline = mocker.Mock(spec=ProductlineAdapter)
    variant = mocker.Mock(spec=VariantAdapter)
    view = CoreViewFactory(productline, variant=variant)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(
        productline, "get_reviews_summary", return_value=reviews_summary
    )
    mocker.patch.object(view, "_get_authors", return_value=authors)
    mocker.patch.object(view, "_get_formats", return_value=formats)

    # set a title for the selected variant
    variant.title = "Test Title - Red"

    output = view.build()

    assert output == CoreView(
        productline_id=123,
        authors=authors,
        formats=formats,
        brand="Test Brand",
        brand_url=BrandUrlLinkData(
            link_data=LinkData(
                path="/all?filter=Brand:{brand_slug}",
                fields={"brand_slug": "Test+Brand"},
            )
        ),
        reviews=10,
        star_rating=4.5,
        slug="test-title",
        title="Test Title - Red",
        subtitle="Test Subtitle",
    )


def test_build_no_author_no_formats(mocker, reviews_summary):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(
        productline, "get_reviews_summary", return_value=reviews_summary
    )

    # We want to see that the coreview is returned if an exception
    # is raised while fetching the formats

    mocker.patch.object(view, "_get_formats", return_value=[]).side_effect = KeyError
    mocker.patch.object(view, "_get_authors", return_value=[])
    output = view.build()

    assert output == CoreView(
        productline_id=123,
        authors=[],
        formats=[],
        brand="Test Brand",
        brand_url=BrandUrlLinkData(
            link_data=LinkData(
                path="/all?filter=Brand:{brand_slug}",
                fields={"brand_slug": "Test+Brand"},
            )
        ),
        reviews=10,
        star_rating=4.5,
        slug="test-title",
        title="Test Title",
        subtitle="Test Subtitle",
    )


def test_build_no_reviews(mocker, authors, formats):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    # mock out some attributes for the test

    productline.productline_id = 123
    productline.title = "Test Title"
    productline.subtitle = "Test Subtitle"
    productline.brand_name = "Test Brand"

    mocker.patch.object(productline, "get_reviews_summary", return_value=None)
    mocker.patch.object(view, "_get_authors", return_value=authors)
    mocker.patch.object(view, "_get_formats", return_value=formats)
    output = view.build()

    assert output == CoreView(
        productline_id=123,
        authors=authors,
        formats=formats,
        brand="Test Brand",
        brand_url=BrandUrlLinkData(
            link_data=LinkData(
                path="/all?filter=Brand:{brand_slug}",
                fields={"brand_slug": "Test+Brand"},
            )
        ),
        reviews=None,
        star_rating=None,
        slug="test-title",
        title="Test Title",
        subtitle="Test Subtitle",
    )


def test_get_authors_no_author_attribute(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    mocker.patch.object(productline, "get_attribute", return_value=None)
    output = view._get_authors()

    assert output == []


def test_get_authors(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    mocker.patch.object(
        productline,
        "get_attribute",
        return_value=Attribute(
            key="author",
            display_name="Test Author",
            display_value="",
            is_displayable=True,
            is_virtual=False,
            value="Test Value Author",
        ),
    )
    output = view._get_authors()

    assert output == [
        Author(
            author_id=-1,
            author="Test Value Author",
            link_data=LinkData(
                path="/all?filter=Author:{author_slug}",
                fields={"author_slug": "Test+Value+Author"},
            ),
        )
    ]


def test_get_authors_author_list(mocker):
    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    mocker.patch.object(
        productline,
        "get_attribute",
        return_value=Attribute(
            key="author",
            display_name="Test Author",
            display_value="",
            is_displayable=True,
            is_virtual=False,
            value=["Test Value Author"],
        ),
    )
    output = view._get_authors()

    assert output == [
        Author(
            author_id=-1,
            author="Test Value Author",
            link_data=LinkData(
                path="/all?filter=Author:{author_slug}",
                fields={"author_slug": "Test+Value+Author"},
            ),
        )
    ]


def test_get_formats(mocker):
    from storefront_product_adapter.adapters.productline import ProductlineAdapter

    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    mocker.patch.object(
        productline,
        "get_attribute_keys",
        return_value={"_weird", "greenNameType_format"},
    )
    mocker.patch.object(
        productline,
        "get_attribute",
        return_value=Attribute(
            key="green",
            display_name="GreenName",
            display_value="",
            is_displayable=True,
            is_virtual=False,
            value=[{"idFormatType": 2, "name": "GreenName", "id": 321}],
        ),
    )

    output = view._get_formats()

    assert output == [
        Format(
            format_type_id=2,
            format_type="Greennametype",
            name="GreenName",
            format_id=321,
            link_data=ContextualLinkData(
                action="search",
                context="navigation",
                parameters={
                    "search": {
                        "filters": {
                            "Available": True,
                            "Format": "GreenName",
                        }
                    }
                },
            ),
        )
    ]


def test_get_formats_attribute_is_displayable_false(mocker):
    from storefront_product_adapter.adapters.productline import ProductlineAdapter

    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    mocker.patch.object(
        productline,
        "get_attribute_keys",
        return_value={"_weird", "greenNameType_format"},
    )
    mocker.patch.object(
        productline,
        "get_attribute",
        return_value=Attribute(
            key="green",
            display_name="GreenName",
            display_value="",
            is_displayable=False,
            is_virtual=False,
            value=[{"idFormatType": 2, "name": "GreenName", "id": 321}],
        ),
    )

    output = view._get_formats()

    assert output == []


def test_get_formats_attribute_not_in_list(mocker):
    from storefront_product_adapter.adapters.productline import ProductlineAdapter

    productline = mocker.Mock(spec=ProductlineAdapter)
    view = CoreViewFactory(productline)
    mocker.patch.object(
        productline,
        "get_attribute_keys",
        return_value={"_weird", "greenNameType_format"},
    )
    mocker.patch.object(
        productline,
        "get_attribute",
        return_value=Attribute(
            key="green",
            display_name="GreenName",
            display_value="",
            is_displayable=True,
            is_virtual=False,
            value={"idFormatType": 2, "name": "GreenName", "id": 321},
        ),
    )

    output = view._get_formats()

    assert output == [
        Format(
            format_type_id=2,
            format_type="Greennametype",
            name="GreenName",
            format_id=321,
            link_data=ContextualLinkData(
                action="search",
                context="navigation",
                parameters={
                    "search": {
                        "filters": {
                            "Available": True,
                            "Format": "GreenName",
                        }
                    }
                },
            ),
        )
    ]


def test_view_to_dict():
    authors = [
        Author(
            author_id=1,
            author="Test Author",
            link_data=LinkData(
                path="/all?filter=Author:{author_slug}",
                fields={"author_slug": "Test Author"},
            ),
        )
    ]
    formats = [
        Format(
            format_type_id=2,
            format_type="Green",
            name="Test name value green",
            format_id=321,
            link_data=ContextualLinkData(
                action="search",
                context="navigation",
                parameters={
                    "search": {
                        "filters": {
                            "Available": True,
                            "Format": "Test+name+value+green",
                        }
                    }
                },
            ),
        )
    ]
    model = CoreView(
        productline_id=123,
        authors=authors,
        formats=formats,
        brand="Test Brand",
        brand_url=BrandUrlLinkData(
            link_data=LinkData(
                path="/all?filter=Brand:{brand_slug}",
                fields={"brand_slug": "Test+Brand"},
            )
        ),
        reviews=10,
        star_rating=4.5,
        slug="test-title",
        title="Test Title",
        subtitle="Test Subtitle",
    )

    output = model.to_dict()
    assert output == {
        "id": 123,
        "authors": [
            {
                "idAuthor": 1,
                "Author": "Test Author",
                "link_data": {
                    "path": "/all?filter=Author:{author_slug}",
                    "fields": {"author_slug": "Test Author"},
                },
            }
        ],
        "formats": [
            {
                "idFormatType": 2,
                "type": "Green",
                "name": "Test name value green",
                "id": 321,
                "link_data": {
                    "action": "search",
                    "context": "navigation",
                    "parameters": {
                        "search": {
                            "filters": {
                                "Available": True,
                                "Format": "Test+name+value+green",
                            }
                        }
                    },
                },
            }
        ],
        "brand": "Test Brand",
        "brand_url": {
            "link_data": {
                "path": "/all?filter=Brand:{brand_slug}",
                "fields": {"brand_slug": "Test+Brand"},
            }
        },
        "reviews": 10,
        "star_rating": 4.5,
        "slug": "test-title",
        "title": "Test Title",
        "subtitle": "Test Subtitle",
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


def test_view_to_dict_simple():
    model = CoreView(
        productline_id=123,
        authors=[],
        formats=[],
        brand=None,
        brand_url=None,
        reviews=10,
        star_rating=4.5,
        slug="test-title",
        title="Test Title",
        subtitle=None,
    )

    output = model.to_dict()
    assert output == {
        "id": 123,
        "authors": [],
        "formats": [],
        "brand": None,
        "brand_url": None,
        "reviews": 10,
        "star_rating": 4.5,
        "slug": "test-title",
        "title": "Test Title",
        "subtitle": None,
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict
