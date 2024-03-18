import copy

from pytest_cases import fixture
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models import catalogue_schema as cat

from tests.views.conftest import _make_savings_offer

BADGES_MOMENT_IN_TIME = "2020-10-15T11:22:33+02:00"


@fixture
def full_cat_doc_for_detail_test_only_two_variants():
    return {
        "productline": {
            "id": 1111,
            "title": "Productline Title 1111",
            "subtitle": "Productline SubTitle 1111",
            "selectors": {"colour": {}, "size": {}},
            "description": "description",
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Summarisor",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 654,
                        "name": "Summarisor",
                        "object": {
                            "image_url": "https://media.takealot.com/brands/summa.gif",
                            "department_ids": [11, 13, 14, 15],
                        },
                        "sort_order": 145400,
                    },
                },
            },
            "dates": {
                "added": "2000-01-01T22:00:00+00:00",
                "expected": None,
                "preorder": None,
                "released": "2000-01-01T22:00:00+00:00",
            },
            "hierarchies": {
                "business": {
                    "forests": [{"id": 6661, "name": "6 6 6 1", "slug": "6-6-6-1"}],
                    "lineages": [
                        [
                            {
                                "id": 5551,
                                "name": "5 5 5 1",
                                "slug": "5-5-5-1",
                                "parent_id": None,
                                "forest_id": 6661,
                            },
                        ]
                    ],
                },
                "taxonomy": {
                    "forests": [{"id": 6662, "name": "6 6 6 2", "slug": "6-6-6-2"}],
                    "lineages": [
                        [
                            {
                                "id": 5552,
                                "name": "5 5 5 2",
                                "slug": "5-5-5-2",
                                "parent_id": None,
                                "forest_id": 6662,
                            },
                        ]
                    ],
                },
                "merchandising": {
                    "forests": [{"id": 6663, "name": "6 6 6 3", "slug": "6-6-6-3"}],
                    "lineages": [
                        [
                            {
                                "id": 5553,
                                "name": "5 5 5 3",
                                "slug": "5-5-5-3",
                                "parent_id": None,
                                "forest_id": 6663,
                            },
                        ]
                    ],
                },
            },
            "images": [
                {
                    "key": "covers_images/1111a/s.file",
                    "url": "http://test.com/ignore.this",
                },
            ],
            "reviews_summary": {
                "total": 1,
                "average_rating": 2,
                "ratings": {"1": 0, "2": 1, "3": 0, "4": 0, "5": 0},
            },
            "pricing": {
                "app": {
                    "price_range": {"min": 2992, "max": 3003},
                },
                "web": {
                    "price_range": {"min": 3002, "max": 3010},
                },
            },
        },
        "variants": {
            "2222": {
                "variant": {
                    "id": 2222,
                    "availability": {"status": "buyable"},
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": "We don't use this",
                            "savings_range": "We don't use this",
                            "selling_price": 1992,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": "We don't use this",
                            "savings_range": "We don't use this",
                            "selling_price": 2002,
                        },
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [3333, 4444, 5555], "used": [6666]},
                            "lowest_priced": {
                                "new": [5555, 4444, 3333],
                                "used": [6666],
                            },
                            "custom_1": {"new": [4444, 3333, 5555], "used": [6666]},
                        },
                        "web": {
                            "fastest": {"new": [3333, 4444, 5555], "used": [6666]},
                            "lowest_priced": {
                                "new": [5555, 4444, 3333],
                                "used": [6666],
                            },
                            "custom_1": {"new": [4444, 3333, 5555], "used": [6666]},
                        },
                    },
                    "selectors": {},
                    "title": "Variant Title 2222",
                },
                "offers": {
                    "3333": {
                        "id": 3333,
                        "availability": {
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2993},
                            "list_price": 4004,
                            "merchant_price": 1001,
                            "web": {"savings_percentage": 0, "selling_price": 3003},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 345,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MerchOfferCode",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                    "4444": {
                        "id": 4444,
                        "availability": {
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2992},
                            "list_price": 4004,
                            "merchant_price": 1001,
                            "web": {"savings_percentage": 0, "selling_price": 3002},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 345,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MerchOfferCode",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                    "5555": {
                        "id": 5555,
                        "availability": {
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2991},
                            "list_price": 4004,
                            "merchant_price": 1001,
                            "web": {"savings_percentage": 0, "selling_price": 3001},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 345,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MerchOfferCode",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                    "6666": {
                        "id": 6666,
                        "availability": {
                            "status": "buyable",
                        },
                        "condition": "used",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2661},
                            "list_price": 4004,
                            "merchant_price": 1001,
                            "web": {"savings_percentage": 0, "selling_price": 3661},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 345,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MerchOfferCode",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                },
            },
            "22221": {
                "variant": {
                    "id": 22221,
                    "availability": {"status": "buyable"},
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": "We don't use this",
                            "savings_range": "We don't use this",
                            "selling_price": 2002,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": "We don't use this",
                            "savings_range": "We don't use this",
                            "selling_price": 2002,
                        },
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [33331, 44441], "used": []},
                            "lowest_priced": {"new": [44441, 33331], "used": []},
                            "custom_1": {"new": [33331, 44441], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [33331, 44441], "used": []},
                            "lowest_priced": {"new": [44441, 33331], "used": []},
                            "custom_1": {"new": [33331, 44441], "used": []},
                        },
                    },
                    "selectors": {},
                    "title": "Variant Title 2222",
                },
                "offers": {
                    "33331": {
                        "id": 33331,
                        "availability": {
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2883},
                            "list_price": 4004,
                            "merchant_price": 1001,
                            "web": {"savings_percentage": 0, "selling_price": 3223},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 345,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MerchOfferCode",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                    "44441": {
                        "id": 44441,
                        "availability": {
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2882},
                            "list_price": 4004,
                            "merchant_price": 1001,
                            "web": {"savings_percentage": 0, "selling_price": 3222},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 345,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MerchOfferCode",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                },
            },
        },
    }


@fixture
def full_cat_doc_for_detail_test_only_one_variant(
    full_cat_doc_for_detail_test_only_two_variants,
):
    source = copy.deepcopy(full_cat_doc_for_detail_test_only_two_variants)
    source["variants"].pop("22221")
    return source


@fixture
def full_cat_doc_for_detail_test_one_variant_used_only(
    full_cat_doc_for_detail_test_only_two_variants,
):
    source = copy.deepcopy(full_cat_doc_for_detail_test_only_two_variants)
    source["variants"].pop("22221")
    buyboxes = source["variants"]["2222"]["variant"]["buyboxes"]
    for platform in ["app", "web"]:
        for buybox_type in ["lowest_priced", "fastest"]:
            buyboxes[platform][buybox_type]["new"] = []
            buyboxes[platform][buybox_type]["new"] = []
    return source


@fixture
def full_cat_doc_for_detail_test_only_one_variant_same_winner(
    full_cat_doc_for_detail_test_only_two_variants,
):
    source = copy.deepcopy(full_cat_doc_for_detail_test_only_two_variants)
    base = source["variants"]["2222"]["variant"]["buyboxes"]["app"]["lowest_priced"]
    source["variants"]["2222"]["variant"]["buyboxes"]["app"]["fastest"] = base
    source["variants"]["2222"]["variant"]["buyboxes"]["web"]["fastest"] = base
    source["variants"]["2222"]["variant"]["buyboxes"]["web"]["lowest_priced"] = base
    source["variants"].pop("22221")
    return source


@fixture
def full_cat_doc_for_detail_test_only_one_variant_out_of_stock(
    full_cat_doc_for_detail_test_only_two_variants,
):
    source = copy.deepcopy(full_cat_doc_for_detail_test_only_two_variants)
    source["variants"].pop("22221")
    source["variants"]["2222"]["variant"]["availability"]["status"] = "non_buyable"

    buyboxes = source["variants"]["2222"]["variant"]["buyboxes"]
    for platform in ["app", "web"]:
        for buybox_type in ["lowest_priced", "fastest"]:
            for condition in ["new", "used"]:
                buyboxes[platform][buybox_type][condition] = []

    for offer_id in ["3333", "4444", "5555", "6666"]:
        offers = source["variants"]["2222"]["offers"]
        offers[offer_id]["availability"]["status"] = "non_buyable"
    return source


@fixture
def full_cat_doc_for_detail_test_only_two_variants_disabled(
    full_cat_doc_for_detail_test_only_two_variants,
):
    source = copy.deepcopy(full_cat_doc_for_detail_test_only_two_variants)

    for variant in source["variants"].values():
        variant["variant"]["availability"]["status"] = "disabled"

        buyboxes = variant["variant"]["buyboxes"]
        for platform in ["app", "web"]:
            for buybox_type in ["lowest_priced", "fastest"]:
                for condition in ["new", "used"]:
                    buyboxes[platform][buybox_type][condition] = []

        for offer in variant["offers"].values():
            offer["availability"]["status"] = "disabled"
    return source


@fixture
def full_cat_doc_for_detail_test_only_two_variants_heavy(
    full_cat_doc_for_detail_test_only_two_variants,
):
    source = copy.deepcopy(full_cat_doc_for_detail_test_only_two_variants)

    for variant in source["variants"].values():
        variant["variant"]["attributes"] = {"has_heavy_charge": {"value": True}}

    return source


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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                        stock=cat.Stock(
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
                            merchant=0,
                        ),
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
                            merchant=0,
                        ),
                    ),
                },
            ),
        },
    )


@fixture
def variant_badges_variants_savings_up_to_12_15(
    src_variants_badges_variants_savings_up_to_12_15,
):
    p = AdaptersFactory.from_productline_lineage(
        src_variants_badges_variants_savings_up_to_12_15
    )
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
                },
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
                    attributes={},
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
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10, "dbn": 10},
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
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10, "dbn": 10},
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
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10},
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
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10},
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
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10},
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
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10},
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
                    attributes={},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                        promotions=[],
                        stock=cat.Stock(
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
def variants_heavy_charge():
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
                "released": "2020-09-16T11:22:33+02:00",
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
                        promotions=[],
                        stock=cat.Stock(
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10, "dbn": 9},
                            merchant=19,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="used",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10, "dbn": 9},
                            merchant=19,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_used():
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
                "released": "2020-09-16T11:22:33+02:00",
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
                    attributes={
                        "has_heavy_charge": cat.Attribute(
                            display_name="Heavy Charge",
                            value=False,
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
                        condition="used",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10),
                            web=cat.OfferPrice(savings_percentage=20),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10, "dbn": 10},
                            merchant=30,
                        ),
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="used",
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                        stock=cat.Stock(
                            warehouses_total=20,
                            warehouse_regions={"cpt": 10, "jhb": 10, "dbn": 10},
                            merchant=30,
                        ),
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variant_not_prepaid(variant_badges_variants_savings_toppick):
    return variant_badges_variants_savings_toppick.variants[1001]


@fixture
def variants_badges_variants_savings_toppick(
    variants_badges_variants_savings_toppick_src,
):
    p = AdaptersFactory.from_productline_lineage(
        variants_badges_variants_savings_toppick_src
    )
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_bad_promotions():
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
                            warehouses_total=10,
                            warehouse_regions={"cpt": 10, "jhb": 0},
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
            warehouses_total=10, warehouse_regions={"cpt": 10, "jhb": 0}, merchant=0
        ),
    )
