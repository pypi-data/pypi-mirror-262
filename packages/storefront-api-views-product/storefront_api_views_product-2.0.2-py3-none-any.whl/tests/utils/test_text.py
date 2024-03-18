import pytest
from storefront_product_adapter.models.pricing import PriceRange, SavingsRange

from storefront_api_views_product.utils import text


@pytest.mark.parametrize(
    ["price_range", "expected"],
    [
        (None, ""),
        (PriceRange(min=67, max=67), "R 67"),
        (PriceRange(min=67, max=77), "From R 67"),
        (PriceRange(min=67000, max=67000), "R 67,000"),
        (PriceRange(min=69999, max=70000), "From R 69,999"),
    ],
)
def test_create_pricing_string(price_range, expected):
    output = text.create_pricing_string(price_range=price_range)

    assert output == expected


@pytest.mark.parametrize(
    ["savings_range", "expected"],
    [
        (None, None),
        (SavingsRange(min=17, max=17), "17%"),
        (SavingsRange(min=17, max=27), "Up to 27%"),
    ],
)
def test_create_savings_string(savings_range, expected):
    output = text.create_savings_string(savings_range=savings_range)

    assert output == expected


@pytest.mark.parametrize(
    ["quantity", "expected"],
    [(None, None), (0, None), (19, "Only 19 left")],
)
def test_create_promotion_quantity_string(quantity, expected):
    output = text.create_promotion_quantity_string(quantity)

    assert output == expected


@pytest.mark.parametrize(
    ["html", "expected", "limit"],
    [
        ("<P>aaa</P><P>bbb</P>", "aaa bbb", None),
        ("<P>aaa</P><P>bbb</P>", "aaa", 4),
        ("<P>aaaasdf</P><P>bbb</P>", "aaaa", 4),
        ("<P>aaa</P><P>basdfbb</P>", "aaa basdfbb", 20),
        ("<P>aaa </P><P>basdfbb</P>", "aaa", 3),
        ("Just some normal text", "Just some normal text", None),
        ("Just some normal text", "Just some", 10),
    ],
)
def test_remove_html_tags_whitespace(html, expected, limit):
    output = text.remove_html_tags_whitespace(potentially_html=html, limit=limit)

    assert output == expected
