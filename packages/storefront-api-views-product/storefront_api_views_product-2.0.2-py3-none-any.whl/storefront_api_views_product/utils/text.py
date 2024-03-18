import re
from typing import Optional

from storefront_product_adapter.models.pricing import PriceRange, SavingsRange

remove_html_tags_rx = re.compile(r"<.*?>", re.DOTALL)
space_rx = re.compile(r"\s+")


def create_single_price_string(price: int) -> str:
    return f"R {price:,}"


def create_pricing_string(price_range: Optional[PriceRange]) -> str:
    """
    Create a pricing string from the given price range
    """

    if not price_range:
        return ""

    if price_range.min == price_range.max:
        return create_single_price_string(price_range.min)

    return f"From R {price_range.min:,}"


def create_savings_string(savings_range: Optional[SavingsRange]) -> Optional[str]:
    """
    Create a savings string from the given savings range, or return `None` if no savings
    are offered
    """

    if not savings_range or savings_range.min == 0:
        return None

    if savings_range.min == savings_range.max:
        return f"{savings_range.min}%"

    return f"Up to {savings_range.max}%"


def create_promotion_quantity_string(quantity: Optional[int]) -> Optional[str]:
    """
    Return the given promotion quantity as a contextualised string for summary views
    only.
    """

    if not quantity:
        return None

    return f"Only {quantity} left"


def remove_html_tags_whitespace(
    potentially_html: str, limit: Optional[int] = None
) -> str:
    """
    A cheaper alternative to using html2text or other fancy
    HTML sanitisers to render HTML to plain text.

    It may be a bit over-eager, but the goal is to keep searchable text.

    Parameters
    ----------
    potentially_html
        Text that is possibly an HTML snippet.
    limit
        A maximum length for the resulting string, attempting to cut on a word boundary.

    Returns
    -------
    Clean, plain text.
    """

    def word_truncate(s: str, limit: int) -> str:
        if len(s) > limit:
            if not s[limit].isspace():
                last_space = s.rfind(" ", 0, limit)
                if last_space != -1:
                    limit = last_space
            s = s[:limit]
        return s

    # First replace all HTML tags with spaces, not empty-string, to ensure
    # that things like "<P>aaa</P><P>bbb</P>" don't become "aaabbb".
    s = remove_html_tags_rx.sub(" ", potentially_html)
    # Then clean up excessive whitespace, either existing or introduced
    # by the above. This also removes line breaks.
    s = space_rx.sub(" ", s).strip()
    if limit:
        s = word_truncate(s, limit)
    return s
