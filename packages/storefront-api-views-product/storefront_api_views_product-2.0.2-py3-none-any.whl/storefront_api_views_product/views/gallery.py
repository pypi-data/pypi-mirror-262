from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from storefront_media_urls.images.products import ProductImages

from .models import BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import ProductlineAdapter, VariantAdapter


@dataclass
class GalleryView(BaseViewModel):
    images: List[str]
    count: int
    display_count: str
    size_guide: Optional[str] = None  # Always `None`, retained for retro-compatibility

    def to_dict(self) -> Dict[str, Any]:
        return {
            "images": self.images,
            "count": self.count,
            "display_count": self.display_count,
            "size_guide": self.size_guide,
        }


class GalleryViewFactory:
    """Search listing Gallery view object for a given productline"""

    def __init__(
        self,
        *,
        productline: ProductlineAdapter,
        variant: Optional[VariantAdapter] = None,
    ) -> None:
        self._productline = productline
        self._variant = variant

    def build(self) -> GalleryView:
        """
        Build and return the `GalleryView` for instance productline.

        > **Note**
        > Returned image paths cannot be used as-is. The `storefront-media-urls` library
        > should be used to convert these to a path that is usable by client frontends.
        """

        images = []

        if cover_image_key := self._get_image_key():
            images.append(ProductImages.build_product_image_url(cover_image_key))
        image_count = len(self._productline.get_image_keys())

        return GalleryView(
            images=images,
            count=image_count,
            display_count=self._create_display_image_count(image_count),
        )

    def _get_image_key(self) -> Optional[str]:
        if self._variant:
            if image_key := self._variant.cover_image_key:
                return image_key

            if colour := self._variant.get_applied_selector_names().colour:
                if images := self._productline.get_colour_selector_image_keys(colour):
                    return images[0]

        return self._productline.cover_image_key

    @staticmethod
    def _create_display_image_count(image_count: int) -> str:
        """
        Create a display count string, from the given integer value.
        """

        return "10+" if image_count > 10 else str(image_count)
