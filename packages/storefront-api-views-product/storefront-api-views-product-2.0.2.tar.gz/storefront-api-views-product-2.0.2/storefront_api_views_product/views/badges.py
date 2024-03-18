from __future__ import annotations

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Container,
    Dict,
    List,
    Optional,
    Tuple,
)

from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from typing_extensions import Final

from ..facades.badges import BadgesFacade
from .models import BadgeType, BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.collections import VariantCollection


"""
This maps the enum to a string that should be displayed in the API response.
Keep the mapping in the view, not the library model.
"""
BADGE_TYPE_MAP: Final[Dict[BadgeType, str]] = {
    BadgeType.IMAGE: "image",
    BadgeType.SAVINGS: "saving",  # Note: Singular in API response
    BadgeType.SOLD_OUT: "sold_out",
    BadgeType.TOP_PICK: "top_pick",
}


@dataclass
class BadgesViewInfo(BaseViewModel):
    # Same as storefront-product-bff/product_bff/models/product_details.py::Badge
    badge_id: str
    badge_type: str
    value: Optional[str] = None
    badge_url_pattern: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        data = {
            "id": self.badge_id,
            "type": self.badge_type,
        }

        if self.value is not None:
            data["value"] = self.value
        if self.badge_url_pattern is not None:
            data["badge_url_pattern"] = self.badge_url_pattern

        return data


@dataclass
class BadgesSummaryView(BaseViewModel):
    entries: List[BadgesViewInfo]
    app_entries: List[BadgesViewInfo]
    promotion_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entries": [e.to_dict() for e in self.entries],
            "app_entries": [e.to_dict() for e in self.app_entries],
            "promotion_id": self.promotion_id,
        }


class BadgesSummaryViewFactory:
    _NEXT_DAY_DELIVERY_BADGE_URL = (
        "https://static.takealot.com/images/badges/next-day-delivery-{view}.png"
    )

    def __init__(
        self,
        *,
        buyable_variants: VariantCollection,
        buybox_type: BuyboxType,
        exclude_badge_types: Optional[Collection[BadgeType]] = None,
        only_promo_ids: Optional[Container[int]] = None,
    ) -> None:
        """
        Build the badges view for a search/summary style response.

        Parameters
        ----------
        buyable_variants
            Ideally a collection of buyable variants, but nothing prevents a user
            from including non_buyable variants. We can investigate deeper to see
            if this actually makes sense or if we should be strict here.
        exclude_badge_types, optional
            Badge types that should not be returned. Note that for a summary view,
            a Sold Out promotion can never show Top Pick or Image badge types so
            excluding Sold Out will only allow a Savings badge.
        only_promo_ids, optional
            Only consider these promotions for badges. For V1, the Search BFF
            would "apply" a promotion filter. Without that filter, Top Pick would
            not be a possible badge type. For V2, we either need to implement that
            same rule here or we expect the caller to add badge exclusions based
            on the context and presence of a promotion filter in the search request.

            For now, None or an empty container of promotion IDs will behave differently
            from V1 and still allow a Top Pick badge.
        """
        self._buyable_variants = buyable_variants
        self.buybox_type = buybox_type
        self._exclude_badge_types = exclude_badge_types
        self._only_promo_ids = only_promo_ids

    def build(self) -> BadgesSummaryView:
        app_entries, app_promotion_id = self._get_entries(Platform.APP)
        web_entries, web_promotion_id = self._get_entries(Platform.WEB)

        return BadgesSummaryView(
            entries=web_entries,
            app_entries=app_entries,
            promotion_id=(
                app_promotion_id if app_promotion_id is not None else web_promotion_id
            ),
        )

    def _get_entries(
        self, platform: Platform
    ) -> Tuple[List[BadgesViewInfo], Optional[int]]:
        badges_facade = BadgesFacade(platform=platform)
        badges = badges_facade.get_summary_badges_from_variants(
            buybox_type=self.buybox_type,
            buyable_variants=self._buyable_variants,
            exclude_badge_types=self._exclude_badge_types,
            only_promo_ids=self._only_promo_ids,
        )

        promotion_id = None
        for badge in badges:
            if badge.promotion_id is not None:
                promotion_id = badge.promotion_id
                break

        return (
            [
                BadgesViewInfo(
                    badge_id=f"badge-{idx}",
                    badge_type=BADGE_TYPE_MAP[badge.badge_type],
                    value=badge.value,
                    badge_url_pattern=badge.url_pattern,
                )
                for idx, badge in enumerate(badges)
            ],
            promotion_id,
        )
