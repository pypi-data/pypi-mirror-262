import json
from dataclasses import dataclass
from typing import Dict, Optional

import pytest
from pytest_cases import parametrize
from storefront_product_adapter.models.buybox import BuyboxType

from storefront_api_views_product.errors import InvalidDataError
from storefront_api_views_product.views.models import (
    Author,
    BaseViewModel,
    BrandUrlLinkData,
    ContextualLinkData,
    Format,
    LinkData,
    OfferPreference,
)


def test_base_view_model__json__(mocker):
    @dataclass
    class ExampleModel(BaseViewModel):
        a: int
        b: int

        def to_dict(self) -> Dict:
            return {"a": self.a, "b": self.b}

    model = ExampleModel(a=1, b=2)
    assert model.__json__(mocker.Mock()) == model.to_dict()
    assert model.__json__(mocker.Mock()) == {"a": 1, "b": 2}


def test_base_view_model_drop_nones(mocker):
    @dataclass
    class ExampleModel(BaseViewModel):
        a: int
        b: Optional[int]
        c: Optional[int] = None

        def to_dict(self) -> Dict:
            return {"a": self.a, "b": self.b, "c": self.c}

    model = ExampleModel(a=1, b=0, c=None)
    output = ExampleModel.drop_nones(model.to_dict())
    assert output == {"a": 1, "b": 0}


def test_link_data_to_dict():
    model = LinkData(path="/{slug}/PLID{plid}", fields={"slug": "test", "plid": "1234"})
    output = model.to_dict()

    assert output == {
        "path": "/{slug}/PLID{plid}",
        "fields": {"slug": "test", "plid": "1234"},
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


def test_contextual_link_data_to_dict():
    model = ContextualLinkData(
        action="search",
        context="navigation",
        parameters={"url": "https://www.takealot.com"},
    )
    output = model.to_dict()

    assert output == {
        "action": "search",
        "context": "navigation",
        "parameters": {"url": "https://www.takealot.com"},
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


def test_brand_url_link_data_to_dict():
    model = BrandUrlLinkData(
        link_data=LinkData(
            path="/{slug}/PLID{plid}", fields={"slug": "test", "plid": "1234"}
        )
    )
    output = model.to_dict()

    assert output == {
        "link_data": {
            "path": "/{slug}/PLID{plid}",
            "fields": {"slug": "test", "plid": "1234"},
        }
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


def test_format_to_dict():
    model = Format(
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
    output = model.to_dict()

    assert output == {
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
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


def test_author_to_dict():
    model = Author(
        author_id=1,
        author="Test Author",
        link_data=LinkData(
            path="/all?filter=Author:{author_slug}",
            fields={"author_slug": "Test Author"},
        ),
    )
    output = model.to_dict()

    assert output == {
        "idAuthor": 1,
        "Author": "Test Author",
        "link_data": {
            "path": "/all?filter=Author:{author_slug}",
            "fields": {"author_slug": "Test Author"},
        },
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict


@parametrize(
    "buybox_type, expected",
    [
        (BuyboxType.FASTEST, OfferPreference.FASTEST),
        (BuyboxType.LOWEST_PRICED, OfferPreference.LOWEST_PRICED),
    ],
)
def test_offer_preference_from_buybux_type(buybox_type, expected):
    assert OfferPreference.from_buybox_type(buybox_type) == expected


def test_offer_preference_from_buybux_type_error():
    with pytest.raises(InvalidDataError):
        OfferPreference.from_buybox_type(BuyboxType.CUSTOM_1)
