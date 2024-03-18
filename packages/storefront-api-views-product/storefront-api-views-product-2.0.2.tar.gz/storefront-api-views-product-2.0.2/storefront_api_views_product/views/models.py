from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional

from storefront_product_adapter.models.buybox import BuyboxType

from storefront_api_views_product.errors import InvalidDataError


class BaseViewModel(metaclass=ABCMeta):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]: ...  # pragma: no cover

    @classmethod
    def drop_nones(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in data.items() if v is not None}

    def __json__(self, request: Any) -> Dict[str, Any]:
        return self.to_dict()


@dataclass
class LinkData(BaseViewModel):
    path: str
    fields: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict:
        return {
            "path": self.path,
            "fields": self.fields,
        }


@dataclass
class ContextualLinkData(BaseViewModel):
    action: str
    context: str
    parameters: Dict[str, Any]

    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "context": self.context,
            "parameters": self.parameters,
        }


@dataclass
class BrandUrlLinkData(BaseViewModel):
    link_data: LinkData

    def to_dict(self) -> Dict:
        return {"link_data": self.link_data.to_dict()}


@dataclass
class Format(BaseViewModel):
    format_type: str
    name: str
    format_id: int
    link_data: ContextualLinkData
    format_type_id: Optional[int]

    def to_dict(self) -> Dict:
        return {
            "type": self.format_type,
            "name": self.name,
            "id": self.format_id,
            "link_data": self.link_data.to_dict(),
            "idFormatType": self.format_type_id,
        }


@dataclass
class Author(BaseViewModel):
    author_id: int
    author: str
    link_data: LinkData

    def to_dict(self) -> Dict:
        return {
            "idAuthor": self.author_id,
            "Author": self.author,
            "link_data": self.link_data.to_dict(),
        }


class InfoType(Enum):
    """
    This enum's values are to be used in API views
    """

    SHORT = "short"
    LONG = "long"


class OfferPreference(Enum):
    """
    This enum's values are to be used in API views when Offer Optimisation is enabled.
    """

    LOWEST_PRICED = "lowest_priced"
    FASTEST = "fastest"

    @classmethod
    def from_buybox_type(cls, buybox_type: BuyboxType) -> OfferPreference:
        if buybox_type == BuyboxType.LOWEST_PRICED:
            return cls.LOWEST_PRICED
        if buybox_type == BuyboxType.FASTEST:
            return cls.FASTEST

        raise InvalidDataError(f"Invalid buybox_type: {buybox_type}")


class BadgeType(Enum):
    SAVINGS = auto()
    IMAGE = auto()
    TOP_PICK = auto()
    SOLD_OUT = auto()
    NEXT_DAY_DELIVERY = auto()


@dataclass
class BadgeInfo:
    """
    For BadgeType IMAGE, TOP_PICK and SOLD_OUT, `promotion_id` is set to the promotion
    that caused this badge to be built.

    `url_pattern` only applies to IMAGE badges,
    """

    badge_type: BadgeType
    value: Optional[str] = None  # This is view stuff, replace with savings_range
    url_pattern: Optional[str] = None
    promotion_id: Optional[int] = None
