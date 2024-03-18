import json

import pytest
from pytest_cases import parametrize_with_cases
from storefront_product_adapter.models.selectors import VariantSelectors

from storefront_api_views_product.views.gallery import GalleryView, GalleryViewFactory

pytestmark = pytest.mark.views


class GalleryBuildCases:
    def case_productline_has_less_than_ten_images(self, mocker):
        image_keys = [
            "covers_images/9cf3bc2a1fca400893a9e514072bcfbe/s.file",
            "covers_images/c6ec911f9d4145c29adf0d2a1ef2d9f8/s.file",
            "covers_images/d9a4cedd71274ba0bd4fbfb7a788d6c8/s.file",
            "covers_images/8252070a100746cfbacef483d407542c/s.file",
            "covers_images/67717b5071ec468eadc455451d8f7b30/s.file",
            "covers_images/63974bc3e0f84ca09e02776c4aed05b3/s.file",
            "covers_images/95426aeb958e45a39dc5d941919189e4/s.file",
            "covers_images/21398afde8544591927efed847725809/s.file",
            "covers_images/865b4527409d4f048b48f4bf2868bb54/s.file",
        ]

        productline = mocker.Mock()
        productline.cover_image_key = (
            "covers_images/95426aeb958e45a39dc5d941919189e4/s.file"
        )
        productline.get_image_keys.return_value = image_keys

        expected = GalleryView(
            images=[
                "https://media.takealot.com/covers_images/95426aeb958e45a39dc5d941919189e4/s-{size}.file"  # noqa: E501
            ],
            count=9,
            display_count="9",
            size_guide=None,
        )

        return productline, expected

    def case_productline_has_more_than_ten_images(self, mocker):
        image_keys = [
            "covers_images/0bda9015e0094cf8b6f593118d0c388b/s.file",
            "covers_images/d254add1b8d748778a777057ac1bf926/s.file",
            "covers_images/4440b25cb2aa4d76a5e2dff8ea3d9af6/s.file",
            "covers_images/c173a072f4e246a895cc334c2221e317/s.file",
            "covers_images/1fe94ca082a746c5adaf3eed04d73236/s.file",
            "covers_images/54b638a8138145cf83b890e5b28dfa5f/s.file",
            "covers_images/9158b053cf774d4e9aab3e92e1ad6375/s.file",
            "covers_images/df18ee7976c647f48f1a85b1d123cd45/s.file",
            "covers_images/c0672f7cf3bf4c0a9630aa386b79d949/s.file",
            "covers_images/17c994d382b543de8299f957558c43f3/s.file",
            "covers_images/70b41696c1ba442c92ad200736ad08a3/s.file",
            "covers_images/93cec394161042c8bf28547e84ad0517/s.file",
            "covers_images/53cfda9948a74f2882ed546d9ac87d00/s.file",
            "covers_images/601990fec6c2432da4ed8f4b326ad9b7/s.file",
            "covers_images/ddb489d281b846ed90e615d22409f9dd/s.file",
            "covers_images/221d5e6050da4789b869fba5357d81d4/s.file",
            "covers_images/facc13f03e344e149de818e765cb385c/s.file",
            "covers_images/8c56a618a3e84ced9d595886707f41d6/s.file",
            "covers_images/cd6d4a4dac204b8e929e1fd7cc200f2f/s.file",
        ]

        productline = mocker.Mock()
        productline.cover_image_key = (
            "covers_images/d254add1b8d748778a777057ac1bf926/s.file"
        )
        productline.get_image_keys.return_value = image_keys

        expected = GalleryView(
            images=[
                "https://media.takealot.com/covers_images/d254add1b8d748778a777057ac1bf926/s-{size}.file"  # noqa: E501
            ],
            count=19,
            display_count="10+",
            size_guide=None,
        )

        return productline, expected

    def case_productline_has_no_images(self, mocker):
        image_keys = []

        productline = mocker.Mock()
        productline.cover_image_key = None
        productline.get_image_keys.return_value = image_keys

        expected = GalleryView(
            images=[],
            count=0,
            display_count="0",
            size_guide=None,
        )

        return productline, expected


@parametrize_with_cases(["productline", "expected"], cases=GalleryBuildCases)
def test_factory_build(productline, expected):
    factory = GalleryViewFactory(productline=productline)
    view = factory.build()

    assert view == expected


class VariantGalleryBuildCases:
    def case_variant_cover_image(self, mocker):
        productline = mocker.Mock()
        productline.cover_image_key = "covers_images/cover-image-1/s.file"
        productline.get_image_keys.return_value = [
            "covers_images/image-1/s.file",
            "covers_images/image-2/s.file",
            "covers_images/image-3/s.file",
        ]

        variant = mocker.Mock()
        variant.cover_image_key = "covers_images/variant-cover-image-1/s.file"

        expected = GalleryView(
            images=[
                "https://media.takealot.com/covers_images/variant-cover-image-1/s-{size}.file"  # noqa: E501
            ],
            count=3,
            display_count="3",
            size_guide=None,
        )

        return productline, variant, expected

    def case_variant_no_cover_image_has_colour_image(self, mocker):
        productline = mocker.Mock()
        productline.cover_image_key = "covers_images/cover-image-1/s.file"
        productline.get_image_keys.return_value = [
            "covers_images/image-1/s.file",
            "covers_images/image-2/s.file",
            "covers_images/image-3/s.file",
        ]
        productline.get_colour_selector_image_keys.return_value = [
            "covers_images/red-image-1/s.file",
            "covers_images/red-image-2/s.file",
        ]

        variant = mocker.Mock()
        variant.cover_image_key = None
        variant.get_applied_selector_names.return_value = VariantSelectors(colour="red")

        expected = GalleryView(
            images=[
                "https://media.takealot.com/covers_images/red-image-1/s-{size}.file"  # noqa: E501
            ],
            count=3,
            display_count="3",
            size_guide=None,
        )

        return productline, variant, expected

    def case_variant_no_cover_image_has_color_but_no_colour_image(self, mocker):
        productline = mocker.Mock()
        productline.cover_image_key = "covers_images/cover-image-1/s.file"
        productline.get_image_keys.return_value = [
            "covers_images/image-1/s.file",
            "covers_images/image-2/s.file",
            "covers_images/image-3/s.file",
        ]
        productline.get_colour_selector_image_keys.return_value = []

        variant = mocker.Mock()
        variant.cover_image_key = None
        variant.get_applied_selector_names.return_value = VariantSelectors(colour="red")

        expected = GalleryView(
            images=[
                "https://media.takealot.com/covers_images/cover-image-1/s-{size}.file"  # noqa: E501
            ],
            count=3,
            display_count="3",
            size_guide=None,
        )

        return productline, variant, expected

    def case_variant_no_cover_image_has_no_color(self, mocker):
        productline = mocker.Mock()
        productline.cover_image_key = "covers_images/cover-image-1/s.file"
        productline.get_image_keys.return_value = [
            "covers_images/image-1/s.file",
            "covers_images/image-2/s.file",
            "covers_images/image-3/s.file",
        ]

        variant = mocker.Mock()
        variant.cover_image_key = None
        variant.get_applied_selector_names.return_value = VariantSelectors()

        expected = GalleryView(
            images=[
                "https://media.takealot.com/covers_images/cover-image-1/s-{size}.file"  # noqa: E501
            ],
            count=3,
            display_count="3",
            size_guide=None,
        )

        return productline, variant, expected


@parametrize_with_cases(
    ["productline", "variant", "expected"], cases=VariantGalleryBuildCases
)
def test_factory_build_variant_cover_image(productline, variant, expected):
    factory = GalleryViewFactory(productline=productline, variant=variant)
    view = factory.build()

    assert view == expected


def test_view_to_dict():
    model = GalleryView(
        images=[
            "https://media.takealot.com/covers_images/95426aeb958e45a39dc5d941919189e4/s-{size}.file"  # noqa: E501
        ],
        count=9,
        display_count="9",
        size_guide=None,
    )
    output = model.to_dict()

    assert output == {
        "images": [
            "https://media.takealot.com/covers_images/95426aeb958e45a39dc5d941919189e4/s-{size}.file"  # noqa: E501
        ],
        "count": 9,
        "display_count": "9",
        "size_guide": None,
    }
    assert json.dumps(output)  # Ensure output is a JSON serializable dict
