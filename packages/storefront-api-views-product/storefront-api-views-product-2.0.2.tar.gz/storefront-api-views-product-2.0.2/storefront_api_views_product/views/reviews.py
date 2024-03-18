from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Optional

from .models import BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.adapters.productline import ProductlineAdapter


@dataclass
class ReviewsDistribution(BaseViewModel):
    num_1_star_ratings: int = 0
    num_2_star_ratings: int = 0
    num_3_star_ratings: int = 0
    num_4_star_ratings: int = 0
    num_5_star_ratings: int = 0

    def to_dict(self) -> Dict:
        return {
            "num_1_star_ratings": self.num_1_star_ratings,
            "num_2_star_ratings": self.num_2_star_ratings,
            "num_3_star_ratings": self.num_3_star_ratings,
            "num_4_star_ratings": self.num_4_star_ratings,
            "num_5_star_ratings": self.num_5_star_ratings,
        }


@dataclass
class ReviewsSummaryView(BaseViewModel):
    star_rating: Optional[float]
    review_count: int
    distribution: ReviewsDistribution

    def to_dict(self) -> Dict:
        return {
            "star_rating": self.star_rating,
            "review_count": self.review_count,
            "distribution": self.distribution.to_dict(),
        }


class ReviewsSummaryViewFactory:
    def __init__(
        self,
        productline: ProductlineAdapter,
    ) -> None:
        self.productline = productline

    def build(self) -> ReviewsSummaryView:
        reviews_summary = self.productline.get_reviews_summary()
        if not reviews_summary:
            return ReviewsSummaryView(
                star_rating=None, review_count=0, distribution=ReviewsDistribution()
            )
        return ReviewsSummaryView(
            star_rating=round(reviews_summary.average_rating, 1) or 0,
            review_count=reviews_summary.total,
            distribution=ReviewsDistribution(
                num_1_star_ratings=reviews_summary.ratings["1"],
                num_2_star_ratings=reviews_summary.ratings["2"],
                num_3_star_ratings=reviews_summary.ratings["3"],
                num_4_star_ratings=reviews_summary.ratings["4"],
                num_5_star_ratings=reviews_summary.ratings["5"],
            ),
        )
