from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List

from .models import BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.collections.variant import VariantCollection


@dataclass
class AppliedSelector:
    key: str
    value: str


@dataclass
class VariantSummaryView(BaseViewModel):
    has_more_colours: bool
    applied_selectors: List[AppliedSelector] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "has_more_colours": self.has_more_colours,
            "applied_selectors": [
                {"key": selector.key, "value": selector.value}
                for selector in self.applied_selectors
            ],
        }


class VariantSummaryViewFactory:
    def __init__(
        self,
        *,
        enabled_variants: VariantCollection,
    ) -> None:
        """
        Buyable and non_buyable variants only. Disabled variants should not
        contribute to this view.

        Productline level selectors can identify disabled variants, so we cannot
        fall back to that level for info.
        """
        self._variants = enabled_variants

    def build(self) -> VariantSummaryView:
        """
        Generate and return a `VariantSummaryView` instance
        """

        has_more_colours = False

        if not self._variants.is_empty():
            selector_filter = self._variants.get_selector_filter()
            if selector_filter.colour and len(selector_filter.colour) > 1:
                has_more_colours = True

        applied_selectors = []
        singular_variant = self._variants.get_singular()
        if singular_variant and singular_variant.get_applied_selector_names():
            applied_selector_names = singular_variant.get_applied_selector_names()

            if applied_selector_names.colour:
                applied_selectors.append(
                    AppliedSelector(
                        key="colour_variant",
                        value=applied_selector_names.colour,
                    )
                )

            if applied_selector_names.size:
                applied_selectors.append(
                    AppliedSelector(
                        key="size",
                        value=applied_selector_names.size,
                    )
                )

        return VariantSummaryView(
            has_more_colours=has_more_colours,
            applied_selectors=applied_selectors,
        )
