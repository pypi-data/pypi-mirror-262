from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Container, Dict, List, Optional

from storefront_product_adapter.models.promotion import Promotion, PromotionGroup

from .models import BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.collections.variant import VariantCollection


@dataclass
class PromotionsSummaryView(BaseViewModel):
    is_displayed: bool
    label: Optional[str]

    def to_dict(self) -> Dict:
        return {"is_displayed": self.is_displayed, "label": self.label}


class PromotionsSummaryViewFactory:
    """This is the promotions summary view factory meant for search results.

    In search results we need to consider all active promotions of all buyable offers.
    """

    def __init__(
        self,
        *,
        buyable_variants: Optional[VariantCollection] = None,
        included_promotion_ids: Optional[Container[int]] = None,
    ) -> None:
        """
        Create the factory

        Parameters
        ----------
        buyable_variants, optional
            Buyable variants. While technically not required, it is preferred to only
            include buyable variants here. Any non_buyable variants will be processed,
            but since they have no buyable offers they won't have any effect.
        included_promotion_ids, optional
            Restrict the view to the given promotion IDs. If None, all promotions
            are used. If empty, no promotions are used.
        """
        self._variants = buyable_variants
        self._included_promotion_ids = included_promotion_ids

    def build(self) -> PromotionsSummaryView:
        promotions = self._get_bundle_promotions()
        if not promotions:
            return PromotionsSummaryView(is_displayed=False, label=None)
        return PromotionsSummaryView(
            is_displayed=bool(promotions),
            label=self._get_promotions_display_label(promotions=promotions),
        )

    def _get_bundle_promotions(self) -> List[Promotion]:
        """
        TODO: Promotions shuffle - DSC-7434 (branch in progress)
        Also, this whole thing really just uses the one promotion in the end, so
        we should not be processing and filtering all these. Figure out if the first
        promotion we use is arbitrary or if it needs to follow a rule, similar to
        badges.
        """
        if not self._variants or self._variants.is_empty():
            return []

        bundle_promos = self._variants.get_active_promotions(
            group_ids=PromotionGroup.bundles()
        )

        """If we are on a search results page built with a specific promotions filter,
        we don't want to show bundle deals that are from other promotions that the page
        is not filtering on. For example, a /deals page for sport bundles should not
        show bundles for back-to-school promotions - maybe some sport socks are also
        being promoted for back-to-school."""
        if self._included_promotion_ids:
            return [
                filtered_promo
                for filtered_promo in bundle_promos
                if filtered_promo.promotion_id in self._included_promotion_ids
            ]
        return bundle_promos

    def _get_promotions_display_label(
        self, promotions: List[Promotion]
    ) -> Optional[str]:
        """
        Return a display label for the given promotion, or a generic label if more
        than one promotion is in the given list
        """
        return (
            promotions[0].display_name
            if len(promotions) == 1
            else "Save with Bundle Deals"
        )
