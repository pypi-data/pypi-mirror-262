from dataclasses import dataclass
from typing import ClassVar, Optional

import pytest
from freezegun import freeze_time
from pytest_cases import parametrize
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.models import catalogue_schema
from storefront_product_adapter.models.stock import PreOrderStatus

from storefront_api_views_product.views.google_structured_data import (
    AggregateRating,
    Author,
    BooksSchema,
    Brand,
    BreadcrumbsSchema,
    Component,
    EntryPoint,
    GsdAvailability,
    ImageObject,
    ItemListElement,
    Offer,
    PageInfo,
    ProductSchema,
    Rating,
    Review,
    ReviewsData,
    ReviewsDataReview,
    ReviewText,
    Schema,
    ViewActionSchema,
)

pytestmark = pytest.mark.views


@dataclass
class NewSchema(Schema):
    _TYPE: ClassVar[str] = "NewSchema"
    item: Optional[int]
    name_with_underscores: Optional[str]
    name_with_id: Optional[int]


@dataclass
class NewComponent(Component):
    _TYPE: ClassVar[str] = "NewComponent"
    item: Optional[int]
    name_with_underscores: Optional[str]
    name_with_id: Optional[int]


@pytest.fixture
def reviews_data_items():
    """
    A sample review model from the reviews integration (before adding `variant_info`)
    """
    return [
        ReviewsDataReview(
            tsin_id=35394507,
            customer_id=5678,
            signature="46e39eb51cd818167b33c0c6aa69d5c7ee3e325f",
            rating=5,
            text=ReviewText(body="No problems here", title="Test Title"),
            uuid="f47f63d1-be96-4a44-a262-a79bd0d049d1",
            num_upvotes=0,
            customer_name="Dosto",
            date="01 Feb 2021",
            time_after_purchase="Reviewed 7 days after purchase",
            variant_info=[],
        )
    ]


@pytest.fixture
def page_info():
    """A sample paging information object"""
    return PageInfo(
        total=75,
        total_pages=8,
        current_page=0,
        page_size=10,
    )


@pytest.fixture
def reviews_data(reviews_data_items, page_info):
    """A sample reviews data result from the reviews integration"""
    return ReviewsData(reviews=reviews_data_items, page_info=page_info)


@pytest.fixture
def source_book_buyable():
    return catalogue_schema.ProductlineLineage(
        productline=catalogue_schema.Productline(
            id=112233,
            attributes={
                "author": {
                    "display_name": "Author",
                    "display_value": ["Julia Quinn"],
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": ["Julia Quinn"],
                },
                "publisher": {
                    "display_name": "Publisher",
                    "display_value": "Piatkus Books",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": "Piatkus Books",
                },
                "published_date": {
                    "display_name": "Published Date",
                    "display_value": "2021-02-04",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": "2021-02-04",
                },
                "book_page_count": {
                    "display_name": "Number of Pages",
                    "display_value": "384",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": 384,
                },
            },
            availability=catalogue_schema.Availability(status="buyable"),
            selectors=catalogue_schema.Selectors(colour={}, size={}),
            reviews_summary=catalogue_schema.ReviewsSummary(
                average_rating=4.5,
                total=6,
                ratings={"1": 0, "2": 0, "3": 0, "4": 3, "5": 3},
            ),
            hierarchies={
                "merchandising": {
                    "lineages": [
                        [
                            {
                                "id": 29728,
                                "name": "Books",
                                "slug": "books-29728",
                                "forest_id": 3,
                            },
                            {
                                "id": 29767,
                                "name": "Fiction",
                                "slug": "fiction-29767",
                                "parent_id": 29728,
                            },
                            {
                                "id": 29789,
                                "name": "Romance",
                                "slug": "romance-29789",
                                "parent_id": 29767,
                            },
                        ]
                    ],
                    "forests": [{"id": 3, "name": "Books", "slug": "books"}],
                }
            },
            description=(
                "The eighth novel in Julia Quinn's globally beloved and bestselling "
                "Bridgerton Family series"
            ),
            title="Bridgertons 08: On The Way To The Wedding (TV Tie-In)",
            images=[{"key": "imgs/QQ/s.file"}],
            dates={
                "added": "2000-02-28T22:00:00+00:00",
                "released": "2000-02-28T22:00:00+00:00",
                "preorder": None,
            },
        ),
        variants={
            12: catalogue_schema.VariantOffers(
                variant=catalogue_schema.Variant(
                    id=12,
                    attributes={},
                    availability=catalogue_schema.Availability(status="buyable"),
                    selectors=catalogue_schema.VariantSelectors(),
                    barcode="9780349429496",
                    title="Bridgertons 08: On The Way To The Wedding (TV Tie-In)",
                    buyboxes={
                        "app": {
                            "fastest": {"new": [2], "used": []},
                            "lowest_priced": {"new": [2], "used": []},
                            "custom_1": {"new": [2], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [2], "used": []},
                            "lowest_priced": {"new": [2], "used": []},
                            "custom_1": {"new": [2], "used": []},
                        },
                    },
                ),
                offers={
                    2: catalogue_schema.Offer(
                        id=2,
                        availability={"status": "buyable"},
                        stock=catalogue_schema.Stock(
                            warehouse_regions={"cpt": 3, "jhb": 1},
                            warehouses_total=122,
                            merchant=0,
                        ),
                        condition="new",
                        pricing=catalogue_schema.OfferPricing(
                            app=catalogue_schema.OfferPrice(
                                savings_percentage=11,
                                selling_price=120,
                            ),
                            list_price=31999,
                            merchant_price=31569,
                            web=catalogue_schema.OfferPrice(
                                savings_percentage=22,
                                selling_price=130,
                            ),
                        ),
                    )
                },
            )
        },
    )


def test_build_view_action(mocker, macbook_productline):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    factory = GoogleStructuredDataFactory(
        productline=macbook_productline, buybox_type=None, reviews_data=None
    )
    output = factory.build_view_action()

    assert output == ViewActionSchema(
        target=EntryPoint(
            url_template=(
                "app://fi.android.takealot/app/takealot.com/product/PLID91107319"
            )
        )
    )


def test_build_book(mocker, source_book_buyable):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    book_productline = AdaptersFactory.from_productline_lineage(source_book_buyable)
    factory = GoogleStructuredDataFactory(
        productline=book_productline, buybox_type=None, reviews_data=None
    )

    output = factory.build_book()
    assert output == BooksSchema(
        isbn="9780349429496",
        author=["Julia Quinn"],
        publisher="Piatkus Books",
        date_published="2021-02-04",
        number_of_pages=384,
    )


def test_build_book_no_isbn(mocker, source_book_buyable):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    source_book_buyable["variants"][12]["variant"]["barcode"] = "1234"

    book_productline = AdaptersFactory.from_productline_lineage(source_book_buyable)
    factory = GoogleStructuredDataFactory(
        productline=book_productline, buybox_type=None, reviews_data=None
    )

    output = factory.build_book()
    assert output is None


def test_build_breadcrumbslist(mocker, macbook_productline):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    factory = GoogleStructuredDataFactory(
        productline=macbook_productline, buybox_type=None, reviews_data=None
    )

    output = factory.build_breadcrumbslist()
    assert output == BreadcrumbsSchema(
        item_list_element=[
            ItemListElement(
                item={
                    "@id": "https://www.takealot.com/computers",
                    "name": "Computers & Tablets",
                },
                position=1,
            ),
            ItemListElement(
                item={
                    "@id": "https://www.takealot.com/computers/laptops-27404",
                    "name": "Laptops",
                },
                position=2,
            ),
            ItemListElement(
                item={
                    "@id": "https://www.takealot.com/computers/notebooks-29051",
                    "name": "Notebooks",
                },
                position=3,
            ),
        ]
    )


@freeze_time("2023-10-13T13:00:00+00:00")
def test_build_product(mocker, macbook_productline, reviews_data):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    factory = GoogleStructuredDataFactory(
        productline=macbook_productline, buybox_type=None, reviews_data=reviews_data
    )

    output = factory.build_product()
    assert output == ProductSchema(
        sku="91107319",
        name=(
            "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD"
        ),
        description="just a description",
        isbn=None,
        gtin13="3600523614455",
        gtin8=None,
        product_id="ean:3600523614455",
        image=[
            ImageObject(
                content_url="https://media.takealot.com/covers_images/123-zoom.file"
            )
        ],
        brand=Brand(name="Apple", logo="https://media.takealot.com/brands/apple.gif"),
        aggregate_rating=AggregateRating(rating_value=4.6, review_count=206),
        review=[
            Review(
                review_rating=Rating(rating_value=5),
                review_body="No problems here",
                author=Author(name="Dosto"),
            )
        ],
        offers=[
            Offer(
                url="https://www.takealot.com/something/PLID91107319",
                availability=["https://schema.org/InStock"],
                price=30499,
                price_currency="ZAR",
                price_valid_until="2023-10-20",
            )
        ],
    )


def test_build_product_with_disabled_products_and_no_brand(
    mocker, full_cat_doc_for_detail_test_only_two_variants_disabled
):
    from storefront_product_adapter.models.buybox import BuyboxType

    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    full_cat_doc_for_detail_test_only_two_variants_disabled["productline"][
        "attributes"
    ] = {}
    productline = AdaptersFactory.from_productline_lineage(
        full_cat_doc_for_detail_test_only_two_variants_disabled
    )
    factory = GoogleStructuredDataFactory(
        productline=productline, buybox_type=BuyboxType.LOWEST_PRICED, reviews_data=None
    )
    output = factory.build_product()
    assert output == ProductSchema(
        sku="1111",
        name="Productline Title 1111",
        description="description",
        isbn=None,
        gtin13=None,
        gtin8=None,
        product_id=None,
        image=[
            ImageObject(
                content_url="https://media.takealot.com/covers_images/1111a/s-zoom.file"
            )
        ],
        brand=None,
        aggregate_rating=AggregateRating(rating_value=2, review_count=1),
        review=None,
        offers=None,
    )


def test_get_gsd_availability_out_of_stock(mocker, macbook_productline):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    mocker.patch.object(
        macbook_productline.availability, "is_buyable", return_value=False
    )
    factory = GoogleStructuredDataFactory(
        productline=macbook_productline, buybox_type=None, reviews_data=None
    )
    output = factory._get_gsd_availability()
    assert output == GsdAvailability.OUT_OF_STOCK


@parametrize(
    "preorder_status, expected",
    [
        (PreOrderStatus.LIVE, GsdAvailability.PRE_ORDER),
        (PreOrderStatus.NOT_LIVE, GsdAvailability.OUT_OF_STOCK),
    ],
)
def test_get_gsd_availability_preorder(
    mocker, macbook_productline, preorder_status, expected
):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    mocker.patch.object(
        macbook_productline, "get_preorder_status", return_value=preorder_status
    )
    factory = GoogleStructuredDataFactory(
        productline=macbook_productline, buybox_type=None, reviews_data=None
    )
    output = factory._get_gsd_availability()
    assert output == expected


def test_get_aggregate_rating_no_reviews_summary(mocker, macbook_productline):
    from storefront_api_views_product.views.google_structured_data import (
        GoogleStructuredDataFactory,
    )

    mocker.patch.object(macbook_productline, "get_reviews_summary", return_value=None)
    factory = GoogleStructuredDataFactory(
        productline=macbook_productline, buybox_type=None, reviews_data=None
    )
    output = factory._get_aggregate_rating()
    assert output is None


@pytest.mark.parametrize(
    ["model", "json"],
    [
        (
            NewComponent(item=1, name_with_underscores="test", name_with_id=123),
            {
                "@type": "NewComponent",
                "item": 1,
                "nameWithUnderscores": "test",
                "nameWithID": 123,
            },
        ),
        (
            NewComponent(item=1, name_with_underscores=None, name_with_id=None),
            {"@type": "NewComponent", "item": 1},
        ),
    ],
)
def test_component(mocker, model, json):
    assert model.__json__(mocker.Mock()) == json


@pytest.mark.parametrize(
    ["model", "json"],
    [
        (
            NewSchema(item=1, name_with_underscores="test", name_with_id=123),
            {
                "@type": "NewSchema",
                "@context": "https://schema.org",
                "item": 1,
                "nameWithUnderscores": "test",
                "nameWithID": 123,
            },
        ),
        (
            NewSchema(item=1, name_with_underscores=None, name_with_id=None),
            {"@type": "NewSchema", "@context": "https://schema.org", "item": 1},
        ),
    ],
)
def test_schema(mocker, model, json):
    assert model.__json__(mocker.Mock()) == json


def test_review_text_json(mocker):
    model = ReviewText(
        body="body",
        title="title",
    )
    assert model.__json__(mocker.Mock()) == {"body": "body", "title": "title"}


def test_review_data_review_json(mocker):
    model = ReviewsDataReview(
        tsin_id=35394507,
        customer_id=5678,
        signature="46e39eb51cd818167b33c0c6aa69d5c7ee3e325f",
        rating=5,
        text=ReviewText(body="No problems here", title="Test Title"),
        uuid="f47f63d1-be96-4a44-a262-a79bd0d049d1",
        num_upvotes=0,
        customer_name="Dosto",
        date="01 Feb 2021",
        time_after_purchase="Reviewed 7 days after purchase",
        variant_info=[],
    )
    assert model.__json__(mocker.Mock()) == {
        "customer_id": 5678,
        "customer_name": "Dosto",
        "date": "01 Feb 2021",
        "num_upvotes": 0,
        "rating": 5,
        "signature": "46e39eb51cd818167b33c0c6aa69d5c7ee3e325f",
        "text": ReviewText(body="No problems here", title="Test Title"),
        "time_after_purchase": "Reviewed 7 days after purchase",
        "tsin_id": 35394507,
        "uuid": "f47f63d1-be96-4a44-a262-a79bd0d049d1",
        "variant_info": [],
    }
