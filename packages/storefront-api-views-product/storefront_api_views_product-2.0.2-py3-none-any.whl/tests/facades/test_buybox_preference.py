import pytest
from pytest_cases import parametrize
from storefront_product_adapter.models.buybox import BuyboxType

from storefront_api_views_product.facades import BuyboxPreferenceFacade

pytestmark = pytest.mark.facades


def test_get_default_for_variants(mocker):
    output = BuyboxPreferenceFacade.get_default_for_variants(variants=mocker.Mock())
    assert output == BuyboxType.LOWEST_PRICED


def test_get_default_for_productline(mocker):
    output = BuyboxPreferenceFacade.get_default_for_productline(
        productline=mocker.Mock()
    )
    assert output == BuyboxType.LOWEST_PRICED


def test_get_default_for_variant(mocker):
    output = BuyboxPreferenceFacade.get_default_for_variant(variant=mocker.Mock())
    assert output == BuyboxType.LOWEST_PRICED


def test_get_default_for_offer(mocker):
    output = BuyboxPreferenceFacade.get_default_for_offer(offer=mocker.Mock())
    assert output == BuyboxType.LOWEST_PRICED


@parametrize(
    "variants_default, expected",
    [
        (BuyboxType.LOWEST_PRICED, [BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST]),
        (BuyboxType.FASTEST, [BuyboxType.FASTEST, BuyboxType.LOWEST_PRICED]),
    ],
)
def test_get_display_preference_for_variants(mocker, variants_default, expected):
    mocker.patch.object(
        BuyboxPreferenceFacade,
        "get_default_for_variants",
        return_value=variants_default,
    )

    output = BuyboxPreferenceFacade.get_display_preference_for_variants(mocker.Mock())

    assert output == expected
