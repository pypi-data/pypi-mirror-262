from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import quote_plus

from storefront_product_adapter.utils.text import TextUtils

from .models import (
    Author,
    BaseViewModel,
    BrandUrlLinkData,
    ContextualLinkData,
    Format,
    LinkData,
)

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import ProductlineAdapter, VariantAdapter


logger = logging.getLogger(__name__)


@dataclass
class CoreView(BaseViewModel):
    productline_id: int
    title: str
    slug: str
    subtitle: Optional[str]
    brand: Optional[str]
    brand_url: Optional[BrandUrlLinkData]
    star_rating: Optional[float]
    reviews: Optional[int]
    formats: List[Format]
    authors: List[Author]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.productline_id,
            "title": self.title,
            "slug": self.slug,
            "subtitle": self.subtitle,
            "brand": self.brand,
            "brand_url": self.brand_url.to_dict() if self.brand_url else None,
            "star_rating": self.star_rating,
            "reviews": self.reviews,
            "formats": [f.to_dict() for f in self.formats],
            "authors": [a.to_dict() for a in self.authors],
        }


class CoreViewFactory:
    def __init__(
        self, productline: ProductlineAdapter, variant: Optional[VariantAdapter] = None
    ) -> None:
        self.productline = productline
        self.variant = variant

    def build(self) -> CoreView:
        """
        Generate and return a `CoreView` instance
        """

        reviews_summary = self.productline.get_reviews_summary()
        reviews_total = None
        reviews_average = None
        if reviews_summary:
            reviews_total = reviews_summary.total
            reviews_average = round(reviews_summary.average_rating, 1)

        brand_name = self.productline.brand_name
        brand_url = self._get_brand_link_data(brand_name) if brand_name else None
        authors = self._get_authors()
        try:
            formats = self._get_formats()
        except Exception:
            # Just make this field empty, don't error the whole thing

            formats = []
            logger.exception("Failed to get core formats data")

        return CoreView(
            productline_id=self.productline.productline_id,
            title=self._get_title(),
            slug=TextUtils.slugify(self.productline.title),
            subtitle=self.productline.subtitle,
            reviews=reviews_total,
            star_rating=reviews_average,
            brand=brand_name,
            brand_url=brand_url,
            authors=authors,
            formats=formats,
        )

    def _get_title(self) -> str:
        if self.variant:
            return self.variant.title
        return self.productline.title

    def _get_brand_link_data(self, brand_name: str) -> BrandUrlLinkData:
        path = "/all?filter=Brand:{brand_slug}"

        brand_url = BrandUrlLinkData(
            link_data=LinkData(path=path, fields={"brand_slug": quote_plus(brand_name)})
        )

        return brand_url

    def _get_authors(self) -> List[Author]:
        """
        This builds a list of Author dataclasses using the same negative IDs and
        plus-escaped slug as SDR did.
        """
        author_attr = self.productline.get_attribute("author")
        authors: List[Author] = []
        if not author_attr or author_attr.value is None:
            return authors

        if isinstance(author_attr.value, str):
            values = [author_attr.value]
        else:
            values = author_attr.value

        for idx, name in enumerate(values):
            authors.append(
                Author(
                    author_id=-(idx + 1),
                    author=name,
                    link_data=LinkData(
                        path="/all?filter=Author:{author_slug}",
                        fields={"author_slug": quote_plus(name)},
                    ),
                )
            )

        return authors

    def _get_formats(self) -> List[Format]:
        """
        This gets productline level attributes that have names ending with `_format`.
        """
        formats: List[Format] = []

        # Get all productline attributes that end with `_format`
        for name in self.productline.get_attribute_keys():
            if not name.endswith("_format"):
                continue

            format_type = name.split("_")[0].capitalize()
            attr = self.productline.get_attribute(name)
            if not attr or not attr.is_displayable:
                # Also check is_displayable, just to make sure we don't
                # grab a very exotic format attribute, like a made-up
                # "warehouse_box_format"
                continue

            values: List[Dict[str, Any]]
            if not isinstance(attr.value, list):
                values = [attr.value]
            else:
                values = attr.value

            for value in values:
                model = self._map_format_value_to_model(
                    value=value, format_type=format_type
                )
                formats.append(model)

        return formats

    def _map_format_value_to_model(self, value: Dict, format_type: str) -> Format:
        """
        Map a "format" attribute value to a `Format` data model, and return this model
        """
        return Format(
            format_type_id=value.get("idFormatType"),
            format_type=format_type,
            name=value["name"],
            format_id=value["id"],
            link_data=ContextualLinkData(
                action="search",
                context="navigation",
                parameters={
                    "search": {
                        "filters": {
                            "Available": True,
                            "Format": quote_plus(value["name"]),
                        }
                    }
                },
            ),
        )
