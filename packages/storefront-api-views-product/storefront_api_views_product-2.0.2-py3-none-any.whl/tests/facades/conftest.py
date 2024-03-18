from pytest_cases import fixture
from storefront_product_adapter.collections.offer import OfferCollection
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models import catalogue_schema as cat
from storefront_product_adapter.models.common import IsoDatesRange
from storefront_product_adapter.models.promotion import Promotion

BADGES_MOMENT_IN_TIME = "2020-10-15T11:22:33+02:00"


@fixture
def mock_dict_two_items(mocker):
    return {
        111: mocker.MagicMock(),
        222: mocker.MagicMock(),
    }


@fixture
def mock_source_with_variants_and_offers():
    return {
        "productline": {
            "id": 1001,
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                    },
                },
                "offers": {
                    80533997: {
                        "id": 80533997,
                        "availability": {"status": "buyable"},
                    }
                },
            },
        },
        "metadata": {
            "cached_timestamp": 112233,
            "indexed_timestamp": 445566.778899,
        },
    }


@fixture
def mock_source_with_variants_and_offers_unboxed_offer():
    return {
        "productline": {
            "id": 1001,
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [], "used": [80533997]},
                            "lowest_priced": {"new": [], "used": [80533997]},
                            "custom_1": {"new": [], "used": [80533997]},
                        },
                        "web": {
                            "fastest": {"new": [], "used": [80533997]},
                            "lowest_priced": {"new": [80533997], "used": [123]},
                            "custom_1": {"new": [], "used": [80533997]},
                        },
                    },
                },
                "offers": {
                    80533997: {
                        "id": 80533997,
                        "availability": {"status": "non_buyable"},
                        "condition": "new",
                    },
                    123: {
                        "id": 123,
                        "availability": {"status": "buyable"},
                        "condition": "used",
                    },
                },
            },
        },
        "metadata": {
            "cached_timestamp": 112233,
            "indexed_timestamp": 445566.778899,
        },
    }


@fixture
def mock_source_with_no_variants_and_offers():
    return {
        "productline": {
            "id": 1001,
        },
        "variants": {},
        "metadata": {
            "cached_timestamp": 112233,
            "indexed_timestamp": 445566.778899,
        },
    }


@fixture
def mock_source_with_variants_and_offers_offer_not_buyable():
    return {
        "productline": {
            "id": 1001,
            "availability": {"status": "non_buyable"},
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "non_buyable"},
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                    },
                },
                "offers": {
                    80533997: {
                        "id": 80533997,
                        "availability": {"status": "non_buyable"},
                        "condition": "unknown",
                    }
                },
            },
        },
        "metadata": {
            "cached_timestamp": 112233,
            "indexed_timestamp": 445566.778899,
        },
    }


@fixture
def mock_source_with_variants_and_dodgy_buybox_offers():
    return {
        "productline": {
            "id": 1001,
            "availability": {"status": "non_buyable"},
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                    },
                },
                "offers": {
                    80533997: {
                        "id": 80533997,
                        "availability": {"status": "non_buyable"},
                        "condition": "unknown",
                    }
                },
            },
        },
        "metadata": {
            "cached_timestamp": 112233,
            "indexed_timestamp": 445566.778899,
        },
    }


@fixture
def mock_source_with_variants_and_offers_offer_disabled():
    return {
        "productline": {
            "id": 1001,
            "availability": {"status": "non_buyable"},
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "non_buyable"},
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [80533997], "used": []},
                            "lowest_priced": {"new": [80533997], "used": []},
                            "custom_1": {"new": [80533997], "used": []},
                        },
                    },
                },
                "offers": {
                    80533997: {
                        "id": 80533997,
                        "availability": {"status": "disabled"},
                        "condition": "unknown",
                        "stock": cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 0,
                                "dbn": 0,
                            },
                            warehouses_total=1,
                            merchant=0,
                        ),
                    }
                },
            },
        },
        "metadata": {
            "cached_timestamp": 112233,
            "indexed_timestamp": 445566.778899,
        },
    }


@fixture
def mock_dict_two_items_with_none(mocker):
    return {
        111: mocker.MagicMock(),
        222: mocker.MagicMock(),
        None: mocker.MagicMock(),
    }


def _make_savings_offer(oid: int, app: int, web: int) -> cat.Offer:
    return cat.Offer(
        id=oid,
        availability=cat.Availability(status="buyable"),
        condition="new",
        pricing=cat.OfferPricing(
            app=cat.OfferPrice(savings_percentage=app),
            web=cat.OfferPrice(savings_percentage=web),
        ),
        promotions=None,
        stock=cat.Stock(
            warehouse_regions={
                "cpt": 10,
                "jhb": 0,
                "dbn": 0,
            },
            warehouses_total=1,
            merchant=0,
        ),
    )


@fixture
def badges_offers_non_buyable():
    return cat.Offer(
        id=1234,
        availability=cat.Availability(status="non_buyable"),
    )


@fixture
def badges_offers_only_savings_12_23():
    return _make_savings_offer(1234, 12, 23)


@fixture
def badges_offers_only_savings_app_12_0():
    return _make_savings_offer(1234, 12, 0)


@fixture
def badges_offers_only_savings_web_0_23():
    return _make_savings_offer(1234, 0, 23)


@fixture
def badges_offers_only_promo_0_0():
    return cat.Offer(
        id=1234,
        availability=cat.Availability(status="buyable"),
        condition="new",
        pricing=cat.OfferPricing(
            app=cat.OfferPrice(savings_percentage=0),
            web=cat.OfferPrice(savings_percentage=0),
        ),
        promotions=[
            cat.Promotion(
                id=1,
                slug="oneone",
                quantity=4,
                price=987,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            )
        ],
        stock=cat.Stock(
            warehouse_regions={
                "cpt": 10,
                "jhb": 0,
                "dbn": 0,
            },
            warehouses_total=10,
            merchant=0,
        ),
    )


@fixture
def badges_offers_promo_and_savings_10_10():
    return cat.Offer(
        id=1234,
        availability=cat.Availability(status="buyable"),
        condition="new",
        pricing=cat.OfferPricing(
            app=cat.OfferPrice(savings_percentage=10),
            web=cat.OfferPrice(savings_percentage=10),
        ),
        promotions=[
            cat.Promotion(
                id=1,
                slug="oneone",
                quantity=4,
                price=987,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            ),
            cat.Promotion(
                id=2,
                slug="twotwo",
                quantity=4,
                price=787,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            ),
        ],
        stock=cat.Stock(
            warehouse_regions={
                "cpt": 0,
                "jhb": 0,
                "dbn": 0,
            },
            warehouses_total=0,
            merchant=0,
        ),
    )


@fixture
def offer_has_stock_in_all_warehouses(badges_offers_promo_and_savings_10_10):
    # Override the stock quantities, as next day delivery requires all warehouses
    # have stock
    badges_offers_promo_and_savings_10_10["stock"] = cat.Stock(
        warehouse_regions={
            "cpt": 10,
            "jhb": 10,
            "dbn": 10,
        },
        warehouses_total=1,
        merchant=0,
    )

    return badges_offers_promo_and_savings_10_10


@fixture
def badges_offers_only_bad_promo_slugs_0_0():
    return cat.Offer(
        id=1234,
        availability=cat.Availability(status="buyable"),
        condition="used",
        pricing=cat.OfferPricing(
            app=cat.OfferPrice(savings_percentage=0),
            web=cat.OfferPrice(savings_percentage=0),
        ),
        promotions=[
            cat.Promotion(
                id=1,
                slug=None,
                quantity=4,
                price=987,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            ),
            cat.Promotion(
                id=1,
                slug="",
                quantity=4,
                price=987,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            ),
            cat.Promotion(
                id=1,
                slug="no-image-badge",
                quantity=4,
                price=987,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            ),
            cat.Promotion(
                id=1,
                slug="npd-abc",
                quantity=4,
                price=987,
                active=True,
                dates=cat.DatesStartEnd(
                    start="2020-10-10T00:00:00+02:00",
                    end="2020-10-20T00:00:00+02:00",
                ),
            ),
        ],
        stock=cat.Stock(
            warehouse_regions={
                "cpt": 10,
                "jhb": 0,
                "dbn": 0,
            },
            warehouses_total=1,
            merchant=0,
        ),
    )


@fixture
def src_variants_badges_variants_savings_up_to_12_15():
    return cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=1, max=15)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=2, max=23)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(
                                new=[1234, 456, 789], used=[]
                            ),
                            fastest=cat.BuyboxVariantList(
                                new=[456, 789, 1234], used=[]
                            ),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[789, 456, 1234], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(
                                new=[789, 1234, 456], used=[]
                            ),
                            fastest=cat.BuyboxVariantList(
                                new=[456, 789, 1234], used=[]
                            ),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1234, 789, 456], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1234": cat.Offer(
                        id=1234,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=12),
                            web=cat.OfferPrice(savings_percentage=23),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=1,
                                slug="oneone",
                                quantity=4,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            )
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 0,
                                "dbn": 0,
                            },
                            warehouses_total=1,
                            merchant=0,
                        ),
                    ),
                    "456": cat.Offer(
                        id=456,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=15),
                            web=cat.OfferPrice(savings_percentage=21),
                        ),
                        promotions=None,
                        stock={
                            "cpt": 10,
                            "jhb": 0,
                            "merchant": 0,
                        },
                    ),
                    "789": cat.Offer(
                        id=789,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=1),
                            web=cat.OfferPrice(savings_percentage=2),
                        ),
                        promotions=None,
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 0,
                                "dbn": 0,
                            },
                            warehouses_total=1,
                            merchant=0,
                        ),
                    ),
                },
            ),
            "1002": cat.VariantOffers(
                variant=cat.Variant(
                    id=1002,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=14)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=12, max=15)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1112, 1113], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1113, 1112], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1112, 1113], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1113, 1112], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1113, 1112], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1112, 1113], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1112": cat.Offer(
                        id=1112,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=12),
                        ),
                        promotions=None,
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 0,
                                "dbn": 0,
                            },
                            warehouses_total=1,
                            merchant=0,
                        ),
                    ),
                    "1113": cat.Offer(
                        id=1113,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=14),
                            web=cat.OfferPrice(savings_percentage=15),
                        ),
                        promotions=None,
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 0,
                                "dbn": 0,
                            },
                            warehouses_total=1,
                            merchant=0,
                        ),
                    ),
                },
            ),
        },
    )


@fixture
def variants_badges_variants_savings_up_to_12_15(
    src_variants_badges_variants_savings_up_to_12_15,
):
    p = AdaptersFactory.from_productline_lineage(
        src_variants_badges_variants_savings_up_to_12_15
    )
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_only_exactly_13_31():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=13, max=13)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=31, max=31)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1332, 1331], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332, 1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1331, 1332], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1331": _make_savings_offer(1331, 13, 31),
                    "1332": _make_savings_offer(1332, 13, 31),
                },
            ),
            "1002": cat.VariantOffers(
                variant=cat.Variant(
                    id=1002,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=13, max=13)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=31, max=31)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1112, 1113], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1113, 1112], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1112, 1113], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1112, 1113], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1113, 1112], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1112, 1113], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1112": _make_savings_offer(1112, 13, 31),
                    "1113": _make_savings_offer(1113, 13, 31),
                },
            ),
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_no_savings():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=0, max=0)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=0, max=0)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1332], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1331": _make_savings_offer(1331, 0, 0),
                    "1332": _make_savings_offer(1332, 0, 0),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_multi_promo():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    attributes={
                        "has_heavy_charge": cat.Attribute(
                            display_name="Heavy Charge",
                            value=False,
                            display_value="No",
                            is_display_attribute=False,
                            is_virtual_attribute=True,
                        )
                    },
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1332, 1331], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332, 1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1331, 1332], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=1,
                                slug="varone",
                                quantity=4,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=2,
                                slug="vartwo",
                                quantity=5,
                                price=980,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=3,
                                slug="varthree",
                                quantity=6,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=4,
                                slug="varfour",
                                quantity=6,
                                price=980,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=5,
                                slug="varfive",
                                quantity=11,
                                price=917,
                                active=False,  # To make sure things skip inactive
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=0,
                        ),
                    ),
                    "1333": cat.Offer(  # Valid, with good promotions, but out of stock
                        id=1333,
                        availability=cat.Availability(status="non_buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=11,
                                slug="varoneone",
                                quantity=14,
                                price=981,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def offers_badges_savings_multi_promo(variants_badges_variants_savings_multi_promo):
    offers = OfferCollection()
    for variant in variants_badges_variants_savings_multi_promo:
        for offer in variant.offers.values():
            offers.add(offer.offer_id, offer)

    return offers


@fixture
def variants_savings_multi_promo_output_1():
    return Promotion(
        promotion_id=1,
        deal_id=None,
        group=None,
        quantity=4,
        active=True,
        position=None,
        product_qualifying_quantity=None,
        promotion_qualifying_quantity=None,
        display_name=None,
        slug="varone",
        dates=IsoDatesRange(
            start="2020-10-10T00:00:00+02:00", end="2020-10-20T00:00:00+02:00"
        ),
        price=987,
        promotion_price=None,
        is_lead_time_allowed=None,
    )


@fixture
def variants_savings_multi_promo_output_2():
    return Promotion(
        promotion_id=2,
        deal_id=None,
        group=None,
        quantity=5,
        active=True,
        position=None,
        product_qualifying_quantity=None,
        promotion_qualifying_quantity=None,
        display_name=None,
        slug="vartwo",
        dates=IsoDatesRange(
            start="2020-10-10T00:00:00+02:00", end="2020-10-20T00:00:00+02:00"
        ),
        price=980,
        promotion_price=None,
        is_lead_time_allowed=None,
    )


@fixture
def variants_savings_multi_promo_output_3():
    return Promotion(
        promotion_id=3,
        deal_id=None,
        group=None,
        quantity=6,
        active=True,
        position=None,
        product_qualifying_quantity=None,
        promotion_qualifying_quantity=None,
        display_name=None,
        slug="varthree",
        dates=IsoDatesRange(
            start="2020-10-10T00:00:00+02:00", end="2020-10-20T00:00:00+02:00"
        ),
        price=987,
        promotion_price=None,
        is_lead_time_allowed=None,
    )


@fixture
def variants_savings_multi_promo_output_4():
    return Promotion(
        promotion_id=4,
        deal_id=None,
        group=None,
        quantity=6,
        active=True,
        position=None,
        product_qualifying_quantity=None,
        promotion_qualifying_quantity=None,
        display_name=None,
        slug="varfour",
        dates=IsoDatesRange(
            start="2020-10-10T00:00:00+02:00", end="2020-10-20T00:00:00+02:00"
        ),
        price=980,
        promotion_price=None,
        is_lead_time_allowed=None,
    )


@fixture
def variants_badges_variants_savings_soldout_promo():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=1,
                                slug="varone",
                                quantity=0,
                                position=2,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            ),
            "1002": cat.VariantOffers(
                variant=cat.Variant(
                    id=1002,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=30, max=30)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=40, max=40)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1333], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1333], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1333], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1333], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1333], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1333], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1333": cat.Offer(
                        id=1333,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=30),
                            web=cat.OfferPrice(savings_percentage=40),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            ),
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_toppick_src():
    return cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                    attributes={
                        "has_heavy_charge": cat.Attribute(
                            display_name="Heavy Charge",
                            value=True,
                            display_value="Yes",
                            is_display_attribute=False,
                            is_virtual_attribute=True,
                        )
                    },
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=1,
                                slug="varone",
                                quantity=8,
                                position=44,
                                price=997,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=123,
                                slug="varonetwothree",
                                quantity=10,
                                position=4,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )


@fixture
def variants_badges_variants_savings_toppick(
    variants_badges_variants_savings_toppick_src,
):
    p = AdaptersFactory.from_productline_lineage(
        variants_badges_variants_savings_toppick_src
    )
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_toppick_no_heavy_charge(
    variants_badges_variants_savings_toppick_src,
):
    variants_badges_variants_savings_toppick_src["variants"]["1001"]["variant"][
        "attributes"
    ] = {
        "has_heavy_charge": cat.Attribute(
            display_name="Heavy Charge",
            value=False,
            display_value="No",
            is_display_attribute=False,
            is_virtual_attribute=True,
        )
    }
    p = AdaptersFactory.from_productline_lineage(
        variants_badges_variants_savings_toppick_src
    )
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_no_promotion_offers():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_two_winning_offers():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332, 1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1331, 1332], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332, 1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1331, 1332], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_non_buyable():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=False,
                ),
            },
            availability=cat.Availability(status="non_buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="non_buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_non_buyable():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
            },
            availability=cat.Availability(status="non_buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="non_buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[], used=[]),
                            fastest=cat.BuyboxVariantList(new=[], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[], used=[]),
                            fastest=cat.BuyboxVariantList(new=[], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="non_buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="non_buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_live_preorder():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": None,
                "released": "2020-11-15T11:22:33+02:00",
                "preorder": "2020-09-15T11:22:33+02:00",
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_digital_product():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=True,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(new=[1331], used=[]),
                        ),
                    ),
                    attributes={
                        "is_prepaid": cat.Attribute(
                            display_name="is_prepaid",
                            display_value="is_prepaid",
                            is_display_attribute=True,
                            is_virtual_attribute=False,
                            value=True,
                        ),
                    },
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="non_buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 00,
                                "dbn": 00,
                            },
                            warehouses_total=10,
                            merchant=0,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_digital_variants():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=True,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=10, max=11)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=20, max=22)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1332, 1331], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332, 1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1331, 1332], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=1,
                                slug="varone",
                                quantity=4,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=2,
                                slug="vartwo",
                                quantity=5,
                                price=980,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=10,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=3,
                                slug="varthree",
                                quantity=6,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=4,
                                slug="varfour",
                                quantity=6,
                                price=980,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=5,
                                slug="varfive",
                                quantity=11,
                                price=917,
                                active=False,  # To make sure things skip inactive
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=10,
                        ),
                    ),
                    "1333": cat.Offer(  # Valid, with good promotions, but out of stock
                        id=1333,
                        availability=cat.Availability(status="non_buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=11,
                                slug="varoneone",
                                quantity=14,
                                price=981,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=10,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_digital_variants_zero_savings_range():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            id=1234,
            hierarchies={
                "merchandising": {
                    "forests": [
                        {
                            "id": 99,
                            "name": "Nine nine",
                            "slug": "_99_",
                        },
                        {
                            "id": 11,
                            "name": "One one",
                            "slug": "_1_1_",
                        },
                        {
                            "id": 22,
                            "name": "Two two",
                        },
                    ]
                }
            },
            attributes={
                "mouse_format": cat.Attribute(
                    display_name="Mouse",
                    display_value="Display this",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value={"name": "Two handed"},
                ),
                "author": cat.Attribute(
                    display_name="Author",
                    display_value="Arthurs",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=["Arthur Dent", "Arthur Bump"],
                ),
                "is_prepaid": cat.Attribute(
                    display_name="is_prepaid",
                    display_value="is_prepaid",
                    is_display_attribute=True,
                    is_virtual_attribute=False,
                    value=True,
                ),
            },
            availability=cat.Availability(status="buyable"),
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
        ),
        variants={
            "1001": cat.VariantOffers(
                variant=cat.Variant(
                    id=1001,
                    availability=cat.Availability(status="buyable"),
                    pricing=cat.VariantPricing(
                        # These in the cat-doc are across all offers
                        app=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=0, max=0)
                        ),
                        web=cat.VariantPrice(
                            savings_range=cat.SavingsRange(min=0, max=0)
                        ),
                    ),
                    buyboxes=cat.Buyboxes(
                        app=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1332, 1331], used=[]
                            ),
                        ),
                        web=cat.BuyboxVariants(
                            custom_1=cat.BuyboxVariantList(new=[1331, 1332], used=[]),
                            fastest=cat.BuyboxVariantList(new=[1332, 1331], used=[]),
                            lowest_priced=cat.BuyboxVariantList(
                                new=[1331, 1332], used=[]
                            ),
                        ),
                    ),
                ),
                offers={
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=0),
                            web=cat.OfferPrice(savings_percentage=0),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=1,
                                slug="varone",
                                quantity=4,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=2,
                                slug="vartwo",
                                quantity=5,
                                price=980,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=10,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=0),
                            web=cat.OfferPrice(savings_percentage=0),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=3,
                                slug="varthree",
                                quantity=6,
                                price=987,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=4,
                                slug="varfour",
                                quantity=6,
                                price=980,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                            cat.Promotion(
                                id=5,
                                slug="varfive",
                                quantity=11,
                                price=917,
                                active=False,  # To make sure things skip inactive
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=10,
                        ),
                    ),
                    "1333": cat.Offer(  # Valid, with good promotions, but out of stock
                        id=1333,
                        availability=cat.Availability(status="non_buyable"),
                        condition="new",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=0),
                            web=cat.OfferPrice(savings_percentage=0),
                        ),
                        promotions=[
                            cat.Promotion(
                                id=11,
                                slug="varoneone",
                                quantity=14,
                                price=981,
                                active=True,
                                dates=cat.DatesStartEnd(
                                    start="2020-10-10T00:00:00+02:00",
                                    end="2020-10-20T00:00:00+02:00",
                                ),
                            ),
                        ],
                        stock=cat.Stock(
                            warehouse_regions={
                                "cpt": 10,
                                "jhb": 10,
                                "dbn": 10,
                            },
                            warehouses_total=30,
                            merchant=10,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def offer_is_prepaid(variants_digital_product):
    return variants_digital_product.variants[1001].offers[1331]


@fixture
def variant_not_prepaid(variants_badges_variants_savings_toppick):
    return variants_badges_variants_savings_toppick.variants[1001]


@fixture
def variant_not_prepaid_no_heavy_charge(
    variants_badges_variants_savings_toppick_no_heavy_charge,
):
    return variants_badges_variants_savings_toppick_no_heavy_charge.variants[1001]
