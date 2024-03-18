from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from storefront_media_urls.images.products import ProductImages, ProductImageSizes
from storefront_product_adapter.facades.hierarchies import HierarchyFacade
from storefront_product_adapter.facades.pricing import PricingFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.availability import AvailabilityStatus
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition
from storefront_product_adapter.models.hierarchies import (
    HierarchyType,
    ImportantDepartments,
)
from storefront_product_adapter.models.stock import PreOrderStatus
from storefront_product_adapter.utils import barcodes
from typing_extensions import TypedDict

from storefront_api_views_product.facades import BuyboxPreferenceFacade
from storefront_api_views_product.utils.text import remove_html_tags_whitespace

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import ProductlineAdapter
    from storefront_product_adapter.models.buybox import BuyboxType


class Component(metaclass=ABCMeta):
    _TYPE: ClassVar[str] = "Unknown"

    def __json__(self, request: Any) -> dict:
        return dict(
            {"@type": self._TYPE},
            **{
                self._to_camelcase(k): v
                for k, v in self.__dict__.items()
                if v is not None
            },
        )

    @staticmethod
    def _to_camelcase(s: str) -> str:
        parts = s.split("_")
        return parts[0].lower() + "".join(
            "ID" if p.lower() == "id" else p.title() for p in parts[1:]
        )


class Schema(Component, metaclass=ABCMeta):
    def __json__(self, request: Any) -> dict:
        data = super().__json__(request)
        data["@context"] = "https://schema.org"
        return data


@dataclass
class EntryPoint(Component):
    _TYPE: ClassVar[str] = "EntryPoint"
    url_template: str


@dataclass
class ImageObject(Component):
    _TYPE: ClassVar[str] = "ImageObject"
    content_url: str


@dataclass
class ViewActionSchema(Schema):
    _TYPE: ClassVar[str] = "ViewAction"
    target: EntryPoint


@dataclass
class AggregateRating(Component):
    _TYPE: ClassVar[str] = "AggregateRating"
    rating_value: float
    review_count: int


@dataclass
class Brand(Component):
    _TYPE: ClassVar[str] = "Brand"
    name: str
    logo: Optional[str]


@dataclass
class Rating(Component):
    _TYPE: ClassVar[str] = "Rating"
    rating_value: int


@dataclass
class Author(Component):
    _TYPE: ClassVar[str] = "Person"
    name: str


@dataclass
class Review(Component):
    _TYPE: ClassVar[str] = "Review"
    review_rating: Rating
    review_body: Optional[str] = None
    author: Optional[Author] = None


@dataclass
class ReviewText:
    body: Optional[str] = None
    title: Optional[str] = None

    def __json__(self, request: Any) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class ReviewsDataReview:
    tsin_id: int
    customer_id: int
    signature: str
    rating: int
    uuid: str
    text: Optional[ReviewText] = None
    num_upvotes: int = 0
    customer_name: Optional[str] = None
    date: Optional[str] = None
    time_after_purchase: Optional[str] = None
    variant_info: list[str] = field(default_factory=list)

    def __json__(self, request: Any) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class PageInfo:
    total: int
    total_pages: int
    current_page: int
    page_size: int


@dataclass
class ReviewsData:
    reviews: list[ReviewsDataReview]
    page_info: PageInfo


@dataclass
class Offer(Component):
    _TYPE: ClassVar[str] = "Offer"
    url: str
    availability: list[str]
    price: int
    price_currency: str
    price_valid_until: str


@dataclass
class ProductSchema(Schema):
    _TYPE: ClassVar[str] = "Product"
    sku: str
    name: str
    description: Optional[str] = None
    isbn: Optional[str] = None
    gtin13: Optional[str] = None
    gtin8: Optional[str] = None
    product_id: Optional[str] = None
    image: Optional[list[ImageObject]] = None
    brand: Optional[Brand] = None
    aggregate_rating: Optional[AggregateRating] = None
    review: Optional[list[Review]] = None
    offers: Optional[list[Offer]] = None


@dataclass
class BooksSchema(Schema):
    _TYPE: ClassVar[str] = "Book"
    isbn: str
    author: Optional[list[str]] = None
    publisher: Optional[str] = None
    date_published: Optional[str] = None
    number_of_pages: Optional[int] = None


Item = TypedDict("Item", {"@id": str, "name": str})


@dataclass
class ItemListElement(Component):
    _TYPE: ClassVar[str] = "ListItem"
    item: Item
    position: int


@dataclass
class BreadcrumbsSchema(Schema):
    _TYPE: ClassVar[str] = "BreadcrumbList"
    item_list_element: list[ItemListElement]


class GsdAvailability(Enum):
    IN_STOCK = "https://schema.org/InStock"
    OUT_OF_STOCK = "https://schema.org/OutOfStock"
    PRE_ORDER = "https://schema.org/PreOrder"


class GoogleStructuredDataFactory:
    def __init__(
        self,
        productline: ProductlineAdapter,
        buybox_type: Optional[BuyboxType],
        reviews_data: Optional[ReviewsData] = None,
    ) -> None:
        self.productline = productline
        self.reviews_summary = self.productline.get_reviews_summary()
        self.reviews_data = reviews_data
        variants = CollectionsFactory.variants_from_productline_adapter(
            self.productline
        )
        enabled_variants = variants.filter_by_availability(
            [AvailabilityStatus.BUYABLE, AvailabilityStatus.NON_BUYABLE]
        )

        self.buybox_type = buybox_type
        if not self.buybox_type:
            self.buybox_type = BuyboxPreferenceFacade.get_default_for_variants(
                enabled_variants
            )

        self.pricing_facade = PricingFacade(
            collections=CollectionsFactory.pricing_from_variants(
                variants=enabled_variants,
                platform=Platform.WEB,
                buybox_type=self.buybox_type,
                buybox_conditions_precedence=[
                    OfferCondition.NEW,
                    OfferCondition.USED,
                ],
            )
        )

        self.price_range = self.pricing_facade.get_display_price_range()

        # Productline level Google Structured Data needs a barcode.
        # Always pick the same variant to avoid random barcode changes.
        self.picked_variant = None
        if not enabled_variants.is_empty():
            self.picked_variant = sorted(enabled_variants.variants.items())[0][1]

        self._set_barcode_information()

    def build_view_action(self) -> ViewActionSchema:
        """Generate a `ViewAction` JSON-LD schema for the product"""
        return ViewActionSchema(
            target=EntryPoint(
                url_template=(
                    f"app://fi.android.takealot/app/takealot.com"
                    f"/product/PLID{self.productline.productline_id}"
                )
            )
        )

    def _get_image_list(self) -> list[ImageObject]:
        # TODO: DSC-7516 - use better image getter, same as Gallery
        # Might need/want to change the class __init__ params to fit better.
        image_list: list[ImageObject] = []
        image_keys = self.productline.get_gallery_image_keys()

        # We are using the Zoom size according to:
        # https://github.com/TAKEALOT/image-providers/blob/5346b2d5033309cf99c1ea7cf5a0b6f288fedc2b/etc/nginx/sites-available/image-provider.conf#L55
        image_size = ProductImageSizes.ZOOM
        for key in image_keys:
            image_url = ProductImages.build_product_image_url(key, size=image_size)
            image_list.append(ImageObject(content_url=image_url))
        return image_list

    def _get_brand_info(self) -> Optional[Brand]:
        brand: Optional[Brand] = None
        brand_attr = self.productline.get_attribute(name="brand")
        if brand_attr and brand_attr.display_value:
            brand = Brand(
                name=brand_attr.display_value,
                logo=brand_attr.value.get("object", {}).get("image_url"),
            )
        return brand

    def _get_aggregate_rating(self) -> Optional[AggregateRating]:
        """
        https://developers.google.com/
            search/docs/appearance/structured-data/review-snippet
        https://schema.org/AggregateRating
        > The highest value allowed in this rating system. If bestRating is omitted,
          5 is assumed.
        """
        if not self.reviews_summary or not self.reviews_summary.total:
            return None

        return AggregateRating(
            rating_value=round(self.reviews_summary.average_rating, 1),
            review_count=self.reviews_summary.total,
        )

    def _get_reviews(self) -> Optional[list[Review]]:
        """Get the list of `Review` JSON-LD components for the given product"""
        if (
            not self.reviews_summary
            or not self.reviews_summary.total
            or not self.reviews_data
        ):
            return None

        return [
            Review(
                review_rating=Rating(review.rating),
                review_body=review.text.body if review.text and index < 30 else None,
                author=Author(name=review.customer_name or "Anonymous"),
            )
            for index, review in enumerate(self.reviews_data.reviews)
            if review.rating
        ]

    def _get_gsd_availability(self) -> GsdAvailability:
        preorder_status = self.productline.get_preorder_status()
        if preorder_status == PreOrderStatus.LIVE:
            return GsdAvailability.PRE_ORDER
        if preorder_status != PreOrderStatus.RELEASED:
            return GsdAvailability.OUT_OF_STOCK

        if self.productline.availability.is_buyable():
            return GsdAvailability.IN_STOCK
        return GsdAvailability.OUT_OF_STOCK

    def _get_offers_info(self) -> Optional[list[Offer]]:
        """Get the list of `Offer` JSON-LD components for the given product"""
        if not self.price_range:
            return None

        offer_price = self.price_range.min

        item_availability = [self._get_gsd_availability()]
        valid_until = (datetime.now() + timedelta(days=7)).date().isoformat()

        relative_url = self.productline.relative_url
        return [
            Offer(
                url=f"https://www.takealot.com{relative_url}",
                availability=[e.value for e in item_availability],
                price=offer_price,
                price_currency="ZAR",
                price_valid_until=valid_until,
            )
        ]

    def _set_barcode_information(self) -> None:
        self.merchandising_hierarchy = HierarchyFacade(
            hierarchy_type=HierarchyType.MERCHANDISING,
            productline=self.productline,
        )
        department_ids = self.merchandising_hierarchy.get_forest_ids()
        is_book = ImportantDepartments.BOOKS in department_ids

        self.gtin13 = None
        self.isbn = None
        self.gsd_product_id = None

        if self.picked_variant:
            barcode = self.picked_variant.barcode
            valid_gtin = barcodes.barcode_to_gtin13(barcode)
            if valid_gtin:
                self.gtin13 = barcode
                self.gsd_product_id = f"ean:{barcode}"
                if is_book and barcodes.is_isbn_prefix(barcode):
                    self.isbn = barcode
                    # Replace the product ID
                    self.gsd_product_id = f"isbn:{barcode}"

    def build_product(self) -> ProductSchema:
        title = self.productline.title
        description = remove_html_tags_whitespace(self.productline.description or title)
        image_list = self._get_image_list()
        brand = self._get_brand_info()
        aggregate_rating = self._get_aggregate_rating()
        reviews = self._get_reviews()

        return ProductSchema(
            sku=str(self.productline.productline_id),
            name=title,
            description=description,
            image=image_list,
            brand=brand,
            aggregate_rating=aggregate_rating,
            review=reviews,
            offers=self._get_offers_info(),
            gtin13=self.gtin13,
            isbn=self.isbn,
            product_id=self.gsd_product_id,
        )

    def build_book(self) -> Optional[BooksSchema]:
        """
        Generate a `Book` JSON-LD schema for the product (only if it is a book)
        """
        if not self.isbn:
            return None

        return BooksSchema(
            isbn=self.isbn,
            author=self.productline.get_attribute_raw_value("author"),
            publisher=self.productline.get_attribute_display_value("publisher"),
            date_published=self.productline.get_attribute_display_value(
                "published_date"
            ),
            number_of_pages=self.productline.get_attribute_raw_value("book_page_count"),
        )

    def build_breadcrumbslist(self) -> BreadcrumbsSchema:
        """Generate a `BreadcrumbList` JSON-LD schema for the product (if it has)"""
        # We use only the primary path to build breadcrumbs.
        base_url = "https://www.takealot.com"
        path = self.merchandising_hierarchy.get_primary_path()
        forest = path.forest
        dept_slug = forest.slug

        breadcrumbs: list[Item] = []
        breadcrumbs = [{"@id": f"{base_url}/{dept_slug}", "name": forest.name}]
        for node in path.nodes:
            breadcrumbs.append(
                {"@id": f"{base_url}/{dept_slug}/{node.slug}", "name": node.name}
            )

        return BreadcrumbsSchema(
            item_list_element=[
                ItemListElement(item=b, position=idx + 1)
                for idx, b in enumerate(breadcrumbs)
            ]
        )
