import copy

import pytest
from pytest_cases import fixture
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models import catalogue_schema as cat


@pytest.fixture
def variant_doc():
    return {
        "productline": {
            "id": 53118185,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "subtitle": None,
            "description": "<p>Test Product Description</p>",
            "relative_url": "Test Relative URL",
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Domestos",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 13750,
                        "name": "Domestos",
                        "object": {
                            "image_url": "test-image.jpg",
                            "department_ids": [8, 12],
                        },
                        "sort_order": 595300,
                    },
                },
                "warranty": {
                    "display_name": "Warranty",
                    "display_value": "Limited (6 months)",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "type": {"id": 2, "name": "Limited", "sort_order": 200},
                        "period": {"unit": "m", "value": 6},
                    },
                },
                "country_of_origin": {
                    "display_name": "Country of Origin",
                    "display_value": "South Africa",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": [
                        {
                            "id": "ZA",
                            "iso3": "ZAF",
                            "name": "South Africa",
                            "sort_order": 17900,
                            "is_subdivision": False,
                        }
                    ],
                },
            },
            "hierarchies": {
                "business": {
                    "lineages": [
                        [
                            {
                                "id": 15485,
                                "name": "Household Cleaning",
                                "slug": "household-cleaning-15485",
                                "parent_id": 15483,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                            {
                                "id": 15483,
                                "name": "Non-Perishable",
                                "slug": "non-perishable-15483",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "taxonomy": {
                    "lineages": [
                        [
                            {
                                "id": 313,
                                "name": "Fresheners & Cleaners",
                                "slug": "fresheners-cleaners-313",
                                "parent_id": 312,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 312,
                                "name": "Bathroom",
                                "slug": "bathroom-312",
                                "parent_id": 311,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 311,
                                "name": "Personal Care",
                                "slug": "personal-care-311",
                                "parent_id": 228,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 2915},
                            },
                            {
                                "id": 228,
                                "name": "Health",
                                "slug": "health-228",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {
                                    "department": 28,
                                    "google_taxonomy": 491,
                                },
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "merchandising": {
                    "lineages": [],
                    "forests": [
                        {"id": 12, "name": "Home & Kitchen", "slug": "home-kitchen"}
                    ],
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "selectors": {"colour": {}, "size": {}},
            "pricing": {
                "web": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": None},
            "dates": {
                "added": "2018-11-07T22:00:00+00:00",
                "released": "2018-11-07T22:00:00+00:00",
                "expected": None,
                "preorder": None,
            },
            "reviews_summary": {
                "total": 1,
                "average_rating": 2,
                "ratings": {"1": 0, "2": 1, "3": 0, "4": 0, "5": 0},
            },
        },
        "variant": {
            "id": 56095806,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "barcode": "06001085010469",
            "attributes": {},
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "pricing": {
                "weighted_average_cost_price": 28.4,
                "historical_selling_price": None,
                "web": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": ""},
            "dates": {"added": "2018-11-07T22:00:00+00:00"},
            "buyboxes": {
                "app": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
                "web": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
            },
            "selectors": {},
        },
        "offers": {
            "81339956": {
                "id": 81339956,
                "barcodes": ["06001085010469", "6001085010469"],
                "condition": "new",
                "merchant_offer_code": "1046",
                "merchant": {
                    "id": 29827662,
                    "type": "supplier",
                    "country": {"iso_code": "ZA"},
                    "status": "active",
                    "leadtime_enabled": False,
                    "display_name": None,
                },
                "leadtime_days": {"min": 5, "max": 7},
                "availability": {"status": "buyable", "reason": "Stock on hand"},
                "condition": "new",
                "stock": {"cpt": 16, "jhb": 25, "merchant": 0},
                "pricing": {
                    "list_price": 42,
                    "merchant_price": 45,
                    "app": {"selling_price": 42, "savings_percentage": 0},
                    "web": {"selling_price": 42, "savings_percentage": 0},
                },
                "dates": {"added": "2018-11-08T15:03:16+00:00"},
                "promotions": [
                    {
                        "id": 76761,
                        "deal_id": 6983591,
                        "group_id": 6,
                        "quantity": 36,
                        "active": True,
                        "position": 999,
                        "product_qualifying_quantity": 0,
                        "promotion_qualifying_quantity": 4,
                        "display_name": "Buy 4 Domestos for R140",
                        "slug": None,
                        "dates": {
                            "start": "2022-11-01T06:30:00+00:00",
                            "end": "2022-11-30T22:00:00+00:00",
                        },
                        "price": 35,
                        "promotion_price": 140,
                        "is_lead_time_allowed": False,
                    },
                    {
                        "id": 75406,
                        "deal_id": 6985513,
                        "group_id": 4,
                        "quantity": 41,
                        "active": True,
                        "position": 999,
                        "product_qualifying_quantity": 0,
                        "promotion_qualifying_quantity": 1,
                        "display_name": "Alot for Less ",
                        "slug": "75406",
                        "dates": {
                            "start": "2022-10-25T04:30:00+00:00",
                            "end": "2022-11-20T21:59:00+00:00",
                        },
                        "price": 42,
                        "promotion_price": None,
                        "is_lead_time_allowed": False,
                    },
                ],
                "condition": "new",
            },
        },
        "metadata": {
            "cached_timestamp": 1668086478,
            "indexed_timestamp": 1656570853.445132,
        },
    }


@pytest.fixture
def variant_doc_no_promotions():
    return {
        "productline": {
            "id": 53118185,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "subtitle": None,
            "description": "<p>Test Product Description</p>",
            "relative_url": "Test Relative URL",
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Domestos",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 13750,
                        "name": "Domestos",
                        "object": {
                            "image_url": "test-image.jpg",
                            "department_ids": [8, 12],
                        },
                        "sort_order": 595300,
                    },
                },
                "warranty": {
                    "display_name": "Warranty",
                    "display_value": "Limited (6 months)",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "type": {"id": 2, "name": "Limited", "sort_order": 200},
                        "period": {"unit": "m", "value": 6},
                    },
                },
                "country_of_origin": {
                    "display_name": "Country of Origin",
                    "display_value": "South Africa",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": [
                        {
                            "id": "ZA",
                            "iso3": "ZAF",
                            "name": "South Africa",
                            "sort_order": 17900,
                            "is_subdivision": False,
                        }
                    ],
                },
            },
            "hierarchies": {
                "business": {
                    "lineages": [
                        [
                            {
                                "id": 15485,
                                "name": "Household Cleaning",
                                "slug": "household-cleaning-15485",
                                "parent_id": 15483,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                            {
                                "id": 15483,
                                "name": "Non-Perishable",
                                "slug": "non-perishable-15483",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "taxonomy": {
                    "lineages": [
                        [
                            {
                                "id": 313,
                                "name": "Fresheners & Cleaners",
                                "slug": "fresheners-cleaners-313",
                                "parent_id": 312,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 312,
                                "name": "Bathroom",
                                "slug": "bathroom-312",
                                "parent_id": 311,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 311,
                                "name": "Personal Care",
                                "slug": "personal-care-311",
                                "parent_id": 228,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 2915},
                            },
                            {
                                "id": 228,
                                "name": "Health",
                                "slug": "health-228",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {
                                    "department": 28,
                                    "google_taxonomy": 491,
                                },
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "merchandising": {
                    "lineages": [],
                    "forests": [
                        {"id": 12, "name": "Home & Kitchen", "slug": "home-kitchen"}
                    ],
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "selectors": {"colour": {}, "size": {}},
            "pricing": {
                "web": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": None},
            "dates": {
                "added": "2018-11-07T22:00:00+00:00",
                "released": "2018-11-07T22:00:00+00:00",
                "expected": None,
                "preorder": None,
            },
            "reviews_summary": {
                "total": 1,
                "average_rating": 2,
                "ratings": {"1": 0, "2": 1, "3": 0, "4": 0, "5": 0},
            },
        },
        "variant": {
            "id": 56095806,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "barcode": "06001085010469",
            "attributes": {
                "volumetric_size": {
                    "display_name": "Volumetric Size",
                    "display_value": "light",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {"id": 1, "name": "light", "sort_order": 100},
                },
                "covid19_sellable": {
                    "display_name": "COVID-19 Sellable",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "wms_is_conveyable": {
                    "display_name": "Is Conveyable",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "cbs_package_weight": {
                    "display_name": "Cubiscan packaged weight",
                    "display_value": "0.84 kg",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {"unit": "kg", "value": 0.84},
                },
                "cbs_package_dimensions": {
                    "display_name": "Cubiscan Packaged dimensions",
                    "display_value": "80.0 x 292.0 x 40.0 mm",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {
                        "unit": "mm",
                        "width": 80,
                        "height": 40,
                        "length": 292,
                    },
                },
                "cbs_measured_volumetric": {
                    "display_name": "Cubiscan Measured Volumetric",
                    "display_value": "934.4",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": 934.4,
                },
                "consolidated_packaged_weight": {
                    "display_name": "Consolidated Packaged Weight",
                    "display_value": "unit: kg, value: 0.84, source: 1",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": {
                        "unit": "kg",
                        "value": 0.84,
                        "source": {"id": 1, "name": "cubiscan", "sort_order": 100},
                    },
                },
                "consolidated_packaged_dimensions": {
                    "display_name": "Consolidated Packaged Dimensions",
                    "display_value": "Test",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": {
                        "unit": "mm",
                        "width": 80,
                        "height": 40,
                        "length": 292,
                        "source": {"id": 1, "name": "cubiscan", "sort_order": 100},
                    },
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "pricing": {
                "weighted_average_cost_price": 28.4,
                "historical_selling_price": None,
                "web": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": ""},
            "dates": {"added": "2018-11-07T22:00:00+00:00"},
            "buyboxes": {
                "app": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
                "web": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
            },
            "selectors": {},
        },
        "offers": {
            "81339956": {
                "id": 81339956,
                "barcodes": ["06001085010469", "6001085010469"],
                "condition": "new",
                "merchant_offer_code": "1046",
                "merchant": {
                    "id": 29827662,
                    "type": "supplier",
                    "country": {"iso_code": "ZA"},
                    "status": "active",
                    "leadtime_enabled": False,
                    "display_name": None,
                },
                "leadtime_days": {"min": 5, "max": 7},
                "availability": {"status": "buyable", "reason": "Stock on hand"},
                "condition": "new",
                "stock": {"cpt": 16, "jhb": 25, "merchant": 0},
                "pricing": {
                    "list_price": 42,
                    "merchant_price": 45,
                    "app": {"selling_price": 42, "savings_percentage": 0},
                    "web": {"selling_price": 42, "savings_percentage": 0},
                },
                "dates": {"added": "2018-11-08T15:03:16+00:00"},
                "promotions": [],
                "condition": "new",
            },
        },
        "metadata": {
            "cached_timestamp": 1668086478,
            "indexed_timestamp": 1656570853.445132,
        },
    }


@pytest.fixture
def variant_doc_multiple_promotions():
    return {
        "productline": {
            "id": 53118185,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "subtitle": None,
            "description": "<p>Test Product Description</p>",
            "relative_url": "Test Relative URL",
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Domestos",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 13750,
                        "name": "Domestos",
                        "object": {
                            "image_url": "test-image.jpg",
                            "department_ids": [8, 12],
                        },
                        "sort_order": 595300,
                    },
                },
                "warranty": {
                    "display_name": "Warranty",
                    "display_value": "Limited (6 months)",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "type": {"id": 2, "name": "Limited", "sort_order": 200},
                        "period": {"unit": "m", "value": 6},
                    },
                },
                "country_of_origin": {
                    "display_name": "Country of Origin",
                    "display_value": "South Africa",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": [
                        {
                            "id": "ZA",
                            "iso3": "ZAF",
                            "name": "South Africa",
                            "sort_order": 17900,
                            "is_subdivision": False,
                        }
                    ],
                },
            },
            "hierarchies": {
                "business": {
                    "lineages": [
                        [
                            {
                                "id": 15485,
                                "name": "Household Cleaning",
                                "slug": "household-cleaning-15485",
                                "parent_id": 15483,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                            {
                                "id": 15483,
                                "name": "Non-Perishable",
                                "slug": "non-perishable-15483",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "taxonomy": {
                    "lineages": [
                        [
                            {
                                "id": 313,
                                "name": "Fresheners & Cleaners",
                                "slug": "fresheners-cleaners-313",
                                "parent_id": 312,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 312,
                                "name": "Bathroom",
                                "slug": "bathroom-312",
                                "parent_id": 311,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 311,
                                "name": "Personal Care",
                                "slug": "personal-care-311",
                                "parent_id": 228,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 2915},
                            },
                            {
                                "id": 228,
                                "name": "Health",
                                "slug": "health-228",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {
                                    "department": 28,
                                    "google_taxonomy": 491,
                                },
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "merchandising": {
                    "lineages": [],
                    "forests": [
                        {"id": 12, "name": "Home & Kitchen", "slug": "home-kitchen"}
                    ],
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "selectors": {"colour": {}, "size": {}},
            "pricing": {
                "web": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": None},
            "dates": {
                "added": "2018-11-07T22:00:00+00:00",
                "released": "2018-11-07T22:00:00+00:00",
                "expected": None,
                "preorder": None,
            },
            "reviews_summary": {
                "total": 1,
                "average_rating": 2,
                "ratings": {"1": 0, "2": 1, "3": 0, "4": 0, "5": 0},
            },
        },
        "variant": {
            "id": 56095806,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "barcode": "06001085010469",
            "attributes": {
                "volumetric_size": {
                    "display_name": "Volumetric Size",
                    "display_value": "light",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {"id": 1, "name": "light", "sort_order": 100},
                },
                "covid19_sellable": {
                    "display_name": "COVID-19 Sellable",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "wms_is_conveyable": {
                    "display_name": "Is Conveyable",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "cbs_package_weight": {
                    "display_name": "Cubiscan packaged weight",
                    "display_value": "0.84 kg",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {"unit": "kg", "value": 0.84},
                },
                "cbs_package_dimensions": {
                    "display_name": "Cubiscan Packaged dimensions",
                    "display_value": "80.0 x 292.0 x 40.0 mm",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {
                        "unit": "mm",
                        "width": 80,
                        "height": 40,
                        "length": 292,
                    },
                },
                "cbs_measured_volumetric": {
                    "display_name": "Cubiscan Measured Volumetric",
                    "display_value": "934.4",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": 934.4,
                },
                "consolidated_packaged_weight": {
                    "display_name": "Consolidated Packaged Weight",
                    "display_value": "unit: kg, value: 0.84, source: 1",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": {
                        "unit": "kg",
                        "value": 0.84,
                        "source": {"id": 1, "name": "cubiscan", "sort_order": 100},
                    },
                },
                "consolidated_packaged_dimensions": {
                    "display_name": "Consolidated Packaged Dimensions",
                    "display_value": "Test",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": {
                        "unit": "mm",
                        "width": 80,
                        "height": 40,
                        "length": 292,
                        "source": {"id": 1, "name": "cubiscan", "sort_order": 100},
                    },
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "pricing": {
                "weighted_average_cost_price": 28.4,
                "historical_selling_price": None,
                "web": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": ""},
            "dates": {"added": "2018-11-07T22:00:00+00:00"},
            "buyboxes": {
                "app": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
                "web": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
            },
            "selectors": {},
        },
        "offers": {
            "81339956": {
                "id": 81339956,
                "barcodes": ["06001085010469", "6001085010469"],
                "condition": "new",
                "merchant_offer_code": "1046",
                "merchant": {
                    "id": 29827662,
                    "type": "supplier",
                    "country": {"iso_code": "ZA"},
                    "status": "active",
                    "leadtime_enabled": False,
                    "display_name": None,
                },
                "leadtime_days": {"min": 5, "max": 7},
                "availability": {"status": "buyable", "reason": "Stock on hand"},
                "condition": "new",
                "stock": {"cpt": 16, "jhb": 25, "merchant": 0},
                "pricing": {
                    "list_price": 42,
                    "merchant_price": 45,
                    "app": {"selling_price": 42, "savings_percentage": 0},
                    "web": {"selling_price": 42, "savings_percentage": 0},
                },
                "dates": {"added": "2018-11-08T15:03:16+00:00"},
                "promotions": [
                    {
                        "id": 76761,
                        "deal_id": 6983591,
                        "group_id": 6,
                        "quantity": 36,
                        "active": True,
                        "position": 999,
                        "product_qualifying_quantity": 0,
                        "promotion_qualifying_quantity": 4,
                        "display_name": "Buy 4 Domestos for R140",
                        "slug": None,
                        "dates": {
                            "start": "2022-11-01T06:30:00+00:00",
                            "end": "2022-11-30T22:00:00+00:00",
                        },
                        "price": 35,
                        "promotion_price": 140,
                        "is_lead_time_allowed": False,
                    },
                    {
                        "id": 75406,
                        "deal_id": 6985513,
                        "group_id": 6,
                        "quantity": 36,
                        "active": True,
                        "position": 999,
                        "product_qualifying_quantity": 0,
                        "promotion_qualifying_quantity": 4,
                        "display_name": "Buy 4 Domestos for R140",
                        "slug": 75406,
                        "dates": {
                            "start": "2022-11-01T06:30:00+00:00",
                            "end": "2022-11-30T22:00:00+00:00",
                        },
                        "price": 35,
                        "promotion_price": 140,
                        "is_lead_time_allowed": False,
                    },
                ],
                "condition": "new",
            },
        },
        "metadata": {
            "cached_timestamp": 1668086478,
            "indexed_timestamp": 1656570853.445132,
        },
    }


@pytest.fixture
def variant_doc_promotion_no_display_name():
    return {
        "productline": {
            "id": 53118185,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "subtitle": None,
            "description": "<p>Test Product Description</p>",
            "relative_url": "Test Relative URL",
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Domestos",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 13750,
                        "name": "Domestos",
                        "object": {
                            "image_url": "test-image.jpg",
                            "department_ids": [8, 12],
                        },
                        "sort_order": 595300,
                    },
                },
                "warranty": {
                    "display_name": "Warranty",
                    "display_value": "Limited (6 months)",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "type": {"id": 2, "name": "Limited", "sort_order": 200},
                        "period": {"unit": "m", "value": 6},
                    },
                },
                "country_of_origin": {
                    "display_name": "Country of Origin",
                    "display_value": "South Africa",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": [
                        {
                            "id": "ZA",
                            "iso3": "ZAF",
                            "name": "South Africa",
                            "sort_order": 17900,
                            "is_subdivision": False,
                        }
                    ],
                },
            },
            "hierarchies": {
                "business": {
                    "lineages": [
                        [
                            {
                                "id": 15485,
                                "name": "Household Cleaning",
                                "slug": "household-cleaning-15485",
                                "parent_id": 15483,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                            {
                                "id": 15483,
                                "name": "Non-Perishable",
                                "slug": "non-perishable-15483",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.005},
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "taxonomy": {
                    "lineages": [
                        [
                            {
                                "id": 313,
                                "name": "Fresheners & Cleaners",
                                "slug": "fresheners-cleaners-313",
                                "parent_id": 312,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 312,
                                "name": "Bathroom",
                                "slug": "bathroom-312",
                                "parent_id": 311,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 474},
                            },
                            {
                                "id": 311,
                                "name": "Personal Care",
                                "slug": "personal-care-311",
                                "parent_id": 228,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 2915},
                            },
                            {
                                "id": 228,
                                "name": "Health",
                                "slug": "health-228",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {
                                    "department": 28,
                                    "google_taxonomy": 491,
                                },
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "merchandising": {
                    "lineages": [],
                    "forests": [
                        {"id": 12, "name": "Home & Kitchen", "slug": "home-kitchen"}
                    ],
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "selectors": {"colour": {}, "size": {}},
            "pricing": {
                "web": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": None},
            "dates": {
                "added": "2018-11-07T22:00:00+00:00",
                "released": "2018-11-07T22:00:00+00:00",
                "expected": None,
                "preorder": None,
            },
            "reviews_summary": {
                "total": 1,
                "average_rating": 2,
                "ratings": {"1": 0, "2": 1, "3": 0, "4": 0, "5": 0},
            },
        },
        "variant": {
            "id": 56095806,
            "title": "Domestos Lemon Fresh Multipurpose Thick Bleach - 750ml",
            "barcode": "06001085010469",
            "attributes": {
                "volumetric_size": {
                    "display_name": "Volumetric Size",
                    "display_value": "light",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {"id": 1, "name": "light", "sort_order": 100},
                },
                "covid19_sellable": {
                    "display_name": "COVID-19 Sellable",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "wms_is_conveyable": {
                    "display_name": "Is Conveyable",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "cbs_package_weight": {
                    "display_name": "Cubiscan packaged weight",
                    "display_value": "0.84 kg",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {"unit": "kg", "value": 0.84},
                },
                "cbs_package_dimensions": {
                    "display_name": "Cubiscan Packaged dimensions",
                    "display_value": "80.0 x 292.0 x 40.0 mm",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": {
                        "unit": "mm",
                        "width": 80,
                        "height": 40,
                        "length": 292,
                    },
                },
                "cbs_measured_volumetric": {
                    "display_name": "Cubiscan Measured Volumetric",
                    "display_value": "934.4",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": 934.4,
                },
                "consolidated_packaged_weight": {
                    "display_name": "Consolidated Packaged Weight",
                    "display_value": "unit: kg, value: 0.84, source: 1",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": {
                        "unit": "kg",
                        "value": 0.84,
                        "source": {"id": 1, "name": "cubiscan", "sort_order": 100},
                    },
                },
                "consolidated_packaged_dimensions": {
                    "display_name": "Consolidated Packaged Dimensions",
                    "display_value": "Test",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": {
                        "unit": "mm",
                        "width": 80,
                        "height": 40,
                        "length": 292,
                        "source": {"id": 1, "name": "cubiscan", "sort_order": 100},
                    },
                },
            },
            "images": [
                {
                    "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                    "url": "http:test.com",
                },
                {
                    "key": "covers_tsins/56095806/06001085010469-1.jpg",
                    "url": "http:test.com",
                },
            ],
            "cover": {
                "key": "covers_images/2636aacbd55c4b48aca79077a6bbdf01/s.file",
                "url": "http:test.com",
            },
            "pricing": {
                "weighted_average_cost_price": 28.4,
                "historical_selling_price": None,
                "web": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
                "app": {
                    "selling_price": 42,
                    "price_range": {"min": 42, "max": 109},
                    "savings_range": {"min": 0, "max": 29},
                },
            },
            "availability": {"status": "buyable", "reason": ""},
            "dates": {"added": "2018-11-07T22:00:00+00:00"},
            "buyboxes": {
                "app": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
                "web": {
                    "fastest": {
                        "new": [
                            81339956,
                            103496916,
                            106076407,
                            107447192,
                            103980637,
                        ],
                        "used": [],
                    },
                    "lowest_priced": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                    "custom_1": {
                        "new": [
                            81339956,
                            103980637,
                            107447192,
                            106076407,
                            103496916,
                        ],
                        "used": [],
                    },
                },
            },
            "selectors": {},
        },
        "offers": {
            "81339956": {
                "id": 81339956,
                "barcodes": ["06001085010469", "6001085010469"],
                "condition": "new",
                "merchant_offer_code": "1046",
                "merchant": {
                    "id": 29827662,
                    "type": "supplier",
                    "country": {"iso_code": "ZA"},
                    "status": "active",
                    "leadtime_enabled": False,
                    "display_name": None,
                },
                "leadtime_days": {"min": 5, "max": 7},
                "availability": {"status": "buyable", "reason": "Stock on hand"},
                "condition": "new",
                "stock": {"cpt": 16, "jhb": 25, "merchant": 0},
                "pricing": {
                    "list_price": 42,
                    "merchant_price": 45,
                    "app": {"selling_price": 42, "savings_percentage": 0},
                    "web": {"selling_price": 42, "savings_percentage": 0},
                },
                "dates": {"added": "2018-11-08T15:03:16+00:00"},
                "promotions": [
                    {
                        "id": 76761,
                        "deal_id": 6983591,
                        "group_id": 6,
                        "quantity": 36,
                        "active": True,
                        "position": 999,
                        "product_qualifying_quantity": 0,
                        "promotion_qualifying_quantity": 4,
                        "display_name": None,
                        "slug": None,
                        "dates": {
                            "start": "2022-11-01T06:30:00+00:00",
                            "end": "2022-11-30T22:00:00+00:00",
                        },
                        "price": 35,
                        "promotion_price": 140,
                        "is_lead_time_allowed": False,
                    },
                    {
                        "id": 75406,
                        "deal_id": 6985513,
                        "group_id": 4,
                        "quantity": 41,
                        "active": True,
                        "position": 999,
                        "product_qualifying_quantity": 0,
                        "promotion_qualifying_quantity": 1,
                        "display_name": None,
                        "slug": "75406",
                        "dates": {
                            "start": "2022-10-25T04:30:00+00:00",
                            "end": "2022-11-20T21:59:00+00:00",
                        },
                        "price": 42,
                        "promotion_price": None,
                        "is_lead_time_allowed": False,
                    },
                ],
                "condition": "new",
            },
        },
        "metadata": {
            "cached_timestamp": 1668086478,
            "indexed_timestamp": 1656570853.445132,
        },
    }


@fixture
def macbook_productline_source():
    return {
        "productline": {
            "id": 91107319,
            "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD",  # noqa: E501
            "description": "just a description",
            "images": [
                {
                    "key": "covers_images/123.file",
                    "url": "http://do.not.use",
                }
            ],
            "availability": {"status": "buyable", "reason": None},
            "relative_url": "/something/PLID91107319",
            "reviews_summary": {
                "total": 206,
                "average_rating": 4.630000114440918,
                "ratings": {"1": 1, "2": 4, "3": 7, "4": 46, "5": 148},
            },
            "selectors": {
                "colour": {"Silver": {}, "Space Grey": {}},
                "size": {},
            },
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Apple",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 198,
                        "name": "Apple",
                        "object": {
                            "image_url": "https://media.takealot.com/brands/apple.gif",
                            "department_ids": [11, 13, 14, 15, 16, 19, 23],
                        },
                        "sort_order": 145400,
                    },
                },
            },
            "dates": {
                "added": "2022-06-22T22:00:00+00:00",
                "expected": None,
                "preorder": "2022-01-22T22:00:00+00:00",
                "released": "2022-06-22T22:00:00+00:00",
            },
            "pricing": {
                "app": {
                    "price_range": {"max": 31569, "min": 30359},
                    "savings_range": {"max": 0, "min": 0},
                },
                "web": {
                    "price_range": {"max": 31569, "min": 30359},
                    "savings_range": {"max": 0, "min": 0},
                },
            },
            "hierarchies": {
                "merchandising": {
                    "lineages": [
                        [
                            {
                                "id": 27404,
                                "name": "Laptops",
                                "slug": "laptops-27404",
                                "forest_id": 13,
                                "parent_id": None,
                                "metadata": {},
                            },
                            {
                                "id": 29051,
                                "name": "Notebooks",
                                "slug": "notebooks-29051",
                                "forest_id": None,
                                "parent_id": 27404,
                                "metadata": {},
                            },
                        ]
                    ],
                    "forests": [
                        {
                            "id": 13,
                            "name": "Computers & Tablets",
                            "slug": "computers",
                        }
                    ],
                }
            },
        },
        "variants": {
            "91245030": {
                "variant": {
                    "id": 91245030,
                    "availability": {"reason": "", "status": "buyable"},
                    "barcode": "3600523614455",
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 30569, "min": 30569},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 30569,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": {"max": 30569, "min": 30569},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 30569,
                        },
                        "weighted_average_cost_price": 25112.46,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [22222222, 202151368], "used": []},
                            "lowest_priced": {"new": [22222222, 202151368], "used": []},
                            "custom_1": {"new": [202151368, 22222222], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [22222222, 202151368], "used": []},
                            "lowest_priced": {"new": [202151368, 22222222], "used": []},
                            "custom_1": {"new": [202151368, 22222222], "used": []},
                        },
                    },
                    "selectors": {"colour": "Space Grey"},
                    "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD - Space Grey",  # noqa: E501
                },
                "offers": {
                    "202151368": {
                        "id": 202151368,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 15, "selling_price": 30359},
                            "list_price": 31999,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 10, "selling_price": 30499},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 513,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MNEJ3ZE/A",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 16, "jhb": 25},
                            "merchant": 0,
                        },
                    },
                    "22222222": {
                        "id": 22222222,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 15, "selling_price": 30333},
                            "list_price": 31888,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 10, "selling_price": 30555},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 555,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "seller",
                        },
                        "merchant_offer_code": "MNEJ3ZE/B",
                        "stock": {
                            "warehouses_total": 41,
                            "warehouse_regions": {"cpt": 1, "jhb": 0},
                            "merchant": 0,
                        },
                    },
                },
            },
            "91245031": {
                "variant": {
                    "id": 91245031,
                    "availability": {"reason": "", "status": "buyable"},
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 31569, "min": 31569},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 31569,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": {"max": 31569, "min": 31569},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 31569,
                        },
                        "weighted_average_cost_price": 24514,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [202151370, 202151369], "used": []},
                            "lowest_priced": {
                                "new": [202151370, 202151369],
                                "used": [],
                            },
                            "custom_1": {"new": [202151369, 202151370], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [202151370, 202151369], "used": []},
                            "lowest_priced": {
                                "new": [202151370, 202151369],
                                "used": [],
                            },
                            "custom_1": {"new": [202151369, 202151370], "used": []},
                        },
                    },
                    "selectors": {"colour": "Silver"},
                    "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD - Silver",  # noqa: E501
                },
                "offers": {
                    "202151369": {
                        "id": 202151369,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 30569},
                            "list_price": 31999,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 0, "selling_price": 31569},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 513,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MNEJ3ZE/A",
                        "stock": {
                            "warehouses_total": 2,
                            "warehouse_regions": {"cpt": 0, "jhb": 2},
                            "merchant": 0,
                        },
                    },
                    "202151370": {
                        # A second offer in a different warehouse, only wins new
                        # buyboxes
                        "id": 202151370,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "new",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 30569},
                            "list_price": 31999,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 0, "selling_price": 31569},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 513,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MNEJ3ZE/A",
                        "stock": {
                            "warehouses_total": 10,
                            "warehouse_regions": {"cpt": 10, "jhb": 0},
                            "merchant": 0,
                        },
                    },
                },
            },
            # A variant with used offers only, should get mostly ignored
            "9991245031": {
                "variant": {
                    "id": 9991245031,
                    "availability": {"reason": "", "status": "buyable"},
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 31569, "min": 31569},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 31569,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": {"max": 31569, "min": 31569},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 31569,
                        },
                        "weighted_average_cost_price": 24514,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [], "used": [99202151369]},
                            "lowest_priced": {
                                "new": [],
                                "used": [99202151369],
                            },
                            "custom_1": {"new": [], "used": [99202151369]},
                        },
                        "web": {
                            "fastest": {"new": [], "used": [99202151369]},
                            "lowest_priced": {
                                "new": [],
                                "used": [99202151369],
                            },
                            "custom_1": {"new": [], "used": [99202151369]},
                        },
                    },
                    "selectors": {"colour": "Silver"},
                    "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD - Silver",  # noqa: E501
                },
                "offers": {
                    "99202151369": {
                        "id": 99202151369,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "used",
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 20569},
                            "list_price": 31999,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 0, "selling_price": 21569},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 513,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MNEJ3ZE/AUUU",
                        "stock": {
                            "warehouses_total": 3,
                            "warehouse_regions": {"cpt": 1, "jhb": 2},
                            "merchant": 0,
                        },
                    },
                },
            },
        },
    }


@fixture
def macbook_productline_preorder_source(macbook_productline_source):
    source = copy.deepcopy(macbook_productline_source)

    source["productline"]["dates"]["released"] = "2333-06-22T22:00:00+00:00"
    source["productline"]["dates"]["preorder"] = "2000-01-22T22:00:00+00:00"
    return source


@fixture
def heavy_charge_macbook_productline_source(macbook_productline_source):
    source = copy.deepcopy(macbook_productline_source)
    source["variants"]["91245031"]["variant"]["attributes"]["has_heavy_charge"] = {
        "value": True
    }
    return source


@fixture
def promotion_of_less_than_twenty_source():
    return [
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 7128876,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 4,
            "id": 75816,
            "is_lead_time_allowed": False,
            "position": 999,
            "price": 3799,
            "product_qualifying_quantity": 1,
            "promotion_price": None,
            "promotion_qualifying_quantity": 1,
            "quantity": 18,
            "slug": "75816",
        }
    ]


@fixture
def promotion_of_more_than_twenty_source():
    return [
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 7128876,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 4,
            "id": 75816,
            "is_lead_time_allowed": False,
            "position": 999,
            "price": 3799,
            "product_qualifying_quantity": 1,
            "promotion_price": None,
            "promotion_qualifying_quantity": 1,
            "quantity": 22,
            "slug": "75816",
        }
    ]


@fixture
def macbook_pro_with_promotion_of_less_than_twenty_source(
    doc_has_only_one_buyable_variant, promotion_of_less_than_twenty_source
):
    doc_copy = copy.deepcopy(doc_has_only_one_buyable_variant)
    doc_copy["variants"]["91245030"]["offers"]["202151368"][
        "promotions"
    ] = promotion_of_less_than_twenty_source

    return doc_copy


@fixture
def macbook_offer_no_listing_price_difference_source(
    macbook_productline_source,
):
    # Base data is:
    # "app": {"savings_percentage": 15, "selling_price": 30359},
    # "list_price": 31999,
    # "merchant_price": 31569,
    # "web": {"savings_percentage": 10, "selling_price": 30499},

    doc_copy = copy.deepcopy(macbook_productline_source)
    doc_copy["variants"]["91245030"]["offers"]["202151368"]["pricing"]["web"][
        "selling_price"
    ] = 31990

    return {
        "productline": doc_copy["productline"],
        "variant": doc_copy["variants"]["91245030"]["variant"],
        "offer": doc_copy["variants"]["91245030"]["offers"]["202151368"],
    }


@fixture
def macbook_productline_single_variant_multi_winner_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245030": doc_copy["variants"]["91245030"]},
    }


@fixture
def macbook_productline_single_variant_single_winner_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245031": doc_copy["variants"]["91245031"]},
    }


@fixture
def macbook_productline_multi_variant_single_winner_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)
    doc_copy["variants"]["91245030"]["variant"]["availability"][
        "status"
    ] = "non_buyable"
    return doc_copy


@fixture
def macbook_productline_single_variant_used_winner_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    return {
        "productline": doc_copy["productline"],
        "variants": {"9991245031": doc_copy["variants"]["9991245031"]},
    }


@fixture
def macbook_productline_single_variant_source_out_of_stock(
    macbook_productline_source_out_of_stock,
):
    doc_copy = copy.deepcopy(macbook_productline_source_out_of_stock)

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245030": doc_copy["variants"]["91245030"]},
    }


@fixture
def macbook_productline_promotion_more_than_twenty_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    doc_copy["variants"]["91245030"]["offers"]["202151368"]["promotions"] = [
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 7128876,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 4,
            "id": 75816,
            "quantity": 22,
        }
    ]

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245030": doc_copy["variants"]["91245030"]},
    }


@fixture
def macbook_productline_promotion_less_than_twenty_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    doc_copy["variants"]["91245030"]["offers"]["202151368"]["promotions"] = [
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 7128876,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 3,  # App Only group for testing shortcut
            "id": 75816,
            "quantity": 16,
        }
    ]

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245030": doc_copy["variants"]["91245030"]},
    }


@fixture
def macbook_productline_multibuy_one_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    doc_copy["variants"]["91245030"]["offers"]["202151368"]["promotions"] = [
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 7128876,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 6,  # Multibuy group
            "id": 75816,
            "quantity": 16,
        }
    ]

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245030": doc_copy["variants"]["91245030"]},
    }


@fixture
def macbook_productline_multibuy_many_source(
    macbook_productline_source,
):
    doc_copy = copy.deepcopy(macbook_productline_source)

    doc_copy["variants"]["91245030"]["offers"]["202151368"]["promotions"] = [
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 7128876,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 6,  # Multibuy group
            "id": 75816,
            "quantity": 16,
        },
        {
            "active": True,
            "dates": {
                "end": "2021-11-24T20:00:00+00:00",
                "start": "2021-11-21T03:00:00+00:00",
            },
            "deal_id": 22222,
            "display_name": "Early Access Tech & Appliances",
            "group_id": 6,  # Multibuy group
            "id": 323,
        },
    ]

    return {
        "productline": doc_copy["productline"],
        "variants": {"91245030": doc_copy["variants"]["91245030"]},
    }


@fixture
def productline_source_size_variance():
    return {
        "productline": {
            "id": 111,
            "title": "One one one",
            "selectors": {
                "colour": {},
                "size": {
                    "Embiggened": {"sort_order": 2},
                    "Cromulised": {"sort_order": 1},
                },
            },
            "attributes": {},
            "dates": {
                "added": "2000-06-22T22:00:00+00:00",
                "preorder": None,
                "released": "2000-06-22T22:00:00+00:00",
            },
            "pricing": {
                "app": {
                    "price_range": {"max": 200, "min": 100},
                    "savings_range": {"max": 0, "min": 0},
                },
                "web": {
                    "price_range": {"max": 200, "min": 100},
                    "savings_range": {"max": 0, "min": 0},
                },
            },
        },
        "variants": {
            "222": {
                "variant": {
                    "id": 222,
                    "availability": {"reason": "", "status": "buyable"},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 200, "min": 200},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 200,
                        },
                        "web": {
                            "price_range": {"max": 200, "min": 200},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 200,
                        },
                        "weighted_average_cost_price": 200,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [333], "used": []},
                            "lowest_priced": {"new": [333], "used": []},
                            "custom_1": {"new": [333], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [333], "used": []},
                            "lowest_priced": {"new": [333], "used": []},
                            "custom_1": {"new": [333], "used": []},
                        },
                    },
                    "selectors": {"size": "Embiggened"},
                    "title": "One one one - Embiggened",
                    "attributes": {},
                },
                "offers": {
                    "333": {
                        "id": 333,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "new",
                        "stock": {"cpt": 16, "jhb": 25, "merchant": 0},
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 200},
                            "list_price": 201,
                            "merchant_price": 201,
                            "web": {"savings_percentage": 0, "selling_price": 200},
                        },
                    },
                },
            },
            "223": {
                "variant": {
                    "id": 223,
                    "availability": {"reason": "", "status": "buyable"},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 100, "min": 100},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 200,
                        },
                        "web": {
                            "price_range": {"max": 100, "min": 100},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 200,
                        },
                        "weighted_average_cost_price": 100,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [334], "used": []},
                            "lowest_priced": {"new": [334], "used": []},
                            "custom_1": {"new": [334], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [334], "used": []},
                            "lowest_priced": {"new": [334], "used": []},
                            "custom_1": {"new": [334], "used": []},
                        },
                    },
                    "selectors": {"size": "Cromulised"},
                    "title": "One one one - Cromulised",
                    "attributes": {},
                },
                "offers": {
                    "334": {
                        "id": 334,
                        "availability": {
                            "reason": "Stock on hand",
                            "status": "buyable",
                        },
                        "condition": "new",
                        "stock": {"cpt": 16, "jhb": 25, "merchant": 0},
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 200},
                            "list_price": 101,
                            "merchant_price": 101,
                            "web": {"savings_percentage": 0, "selling_price": 200},
                        },
                    },
                },
            },
        },
    }


@fixture
def macbook_productline_source_out_of_stock():
    return {
        "productline": {
            "id": 91107319,
            "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD",  # noqa: E501
            "selectors": {
                "colour": {"Silver": {}, "Space Grey": {}},
                "size": {},
            },
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Apple",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 198,
                        "name": "Apple",
                        "object": {
                            "image_url": "https://media.takealot.com/brands/apple.gif",
                            "department_ids": [11, 13, 14, 15, 16, 19, 23],
                        },
                        "sort_order": 145400,
                    },
                },
            },
            "dates": {
                "added": "2022-06-22T22:00:00+00:00",
                "expected": None,
                "preorder": None,
                "released": "2022-06-22T22:00:00+00:00",
            },
            "hierarchies": {
                "merchandising": {
                    "lineages": [
                        [
                            {
                                "id": 27404,
                                "name": "Laptops",
                                "slug": "laptops-27404",
                                "forest_id": 13,
                                "parent_id": None,
                                "metadata": {},
                            },
                            {
                                "id": 29051,
                                "name": "Notebooks",
                                "slug": "notebooks-29051",
                                "forest_id": None,
                                "parent_id": 27404,
                                "metadata": {},
                            },
                        ]
                    ],
                    "forests": [
                        {
                            "id": 13,
                            "name": "Computers & Tablets",
                            "slug": "computers",
                        }
                    ],
                }
            },
            "pricing": {
                "app": {
                    "price_range": {"max": 2, "min": 1},
                    "savings_range": {"max": 0, "min": 0},
                },
                "web": {
                    "price_range": {"max": 2, "min": 1},
                    "savings_range": {"max": 0, "min": 0},
                },
            },
        },
        "variants": {
            "91245030": {
                "variant": {
                    "id": 91245030,
                    "availability": {"status": "non_buyable"},
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 2, "min": 1},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 2,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": {"max": 2, "min": 1},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 1,
                        },
                        "weighted_average_cost_price": 25112.46,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [], "used": []},
                            "lowest_priced": {"new": [], "used": []},
                            "custom_1": {"new": [], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [], "used": []},
                            "lowest_priced": {"new": [], "used": []},
                            "custom_1": {"new": [], "used": []},
                        },
                    },
                    "selectors": {"colour": "Space Grey"},
                    "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD - Space Grey",  # noqa: E501
                },
                "offers": {
                    "202151368": {
                        "id": 202151368,
                        "availability": {
                            "status": "non_buyable",
                        },
                        "condition": "new",
                        "stock": {"cpt": 0, "jhb": 0, "merchant": 0},
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 2},
                            "list_price": 31999,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 10, "selling_price": 1},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 513,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MNEJ3ZE/A",
                    },
                },
            },
            "91245031": {
                "variant": {
                    "id": 91245031,
                    "availability": {"status": "non_buyable"},
                    "attributes": {},
                    "pricing": {
                        "app": {
                            "price_range": {"max": 4, "min": 3},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 3,
                        },
                        "historical_selling_price": None,
                        "web": {
                            "price_range": {"max": 4, "min": 3},
                            "savings_range": {"max": 0, "min": 0},
                            "selling_price": 4,
                        },
                        "weighted_average_cost_price": 24514,
                    },
                    "buyboxes": {
                        "app": {
                            "fastest": {"new": [], "used": []},
                            "lowest_priced": {"new": [], "used": []},
                            "custom_1": {"new": [], "used": []},
                        },
                        "web": {
                            "fastest": {"new": [], "used": []},
                            "lowest_priced": {"new": [], "used": []},
                            "custom_1": {"new": [], "used": []},
                        },
                    },
                    "selectors": {"colour": "Silver"},
                    "title": "Apple MacBook Pro 13inch M2 chip with 8-core CPU and 10-core GPU 512GB SSD - Silver",  # noqa: E501
                },
                "offers": {
                    "202151369": {
                        "id": 202151369,
                        "availability": {
                            "status": "non_buyable",
                        },
                        "condition": "new",
                        "stock": {"cpt": 0, "jhb": 0, "merchant": 0},
                        "pricing": {
                            "app": {"savings_percentage": 0, "selling_price": 3},
                            "list_price": 31999,
                            "merchant_price": 31569,
                            "web": {"savings_percentage": 0, "selling_price": 4},
                        },
                        "promotions": [],
                        "merchant": {
                            "country": {"iso_code": "ZA"},
                            "display_name": None,
                            "id": 513,
                            "leadtime_enabled": False,
                            "status": "active",
                            "type": "supplier",
                        },
                        "merchant_offer_code": "MNEJ3ZE/A",
                    },
                },
            },
        },
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
            warehouse_regions={"cpt": 0, "jhb": 0}, warehouses_total=0, merchant=0
        ),
    )


@fixture
def variants_badges_variants_savings_up_to_12_15():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
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
                    attributes={},
                ),
                offers={
                    "1234": _make_savings_offer(1234, 12, 23),
                    "456": _make_savings_offer(456, 15, 21),
                    "789": _make_savings_offer(789, 1, 2),
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
                    "1112": _make_savings_offer(1112, 10, 12),
                    "1113": _make_savings_offer(1113, 14, 15),
                },
            ),
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_multi_promo():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
            hierarchies=cat.ProductlineHierarchies(
                merchandising=cat.Hierarchy(
                    forests=[cat.HierarchyForest(id=1, name="1", slug="1")]
                )
            ),
            attributes={},
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
                    "1331": cat.Offer(
                        id=1331,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        stock=cat.Stock(
                            warehouse_regions={"cpt": 5, "jhb": 2, "dbn": 1},
                            warehouses_total=7,
                            merchant=0,
                        ),
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=10, selling_price=10),
                            web=cat.OfferPrice(savings_percentage=20, selling_price=10),
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
                        attributes={},
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        stock=cat.Stock(
                            warehouse_regions={"cpt": 5, "jhb": 2, "dbn": 1},
                            warehouses_total=7,
                            merchant=0,
                        ),
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11, selling_price=10),
                            web=cat.OfferPrice(savings_percentage=22, selling_price=10),
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
                        ],
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_soldout_promo():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
            hierarchies=cat.ProductlineHierarchies(
                merchandising=cat.Hierarchy(
                    forests=[cat.HierarchyForest(id=1, name="1", slug="1")]
                )
            ),
            attributes={},
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
                    ),
                },
            ),
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture
def variants_badges_variants_savings_toppick():
    src = cat.ProductlineLineage(
        productline=cat.Productline(
            dates={
                "added": "2002-07-18 00:00:00",
                "expected": "2004-05-07 00:00:00",
                "released": "2004-05-24 00:00:00",
                "preorder": None,
            },
            hierarchies=cat.ProductlineHierarchies(
                merchandising=cat.Hierarchy(
                    forests=[cat.HierarchyForest(id=1, name="1", slug="1")]
                )
            ),
            attributes={},
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
                        stock=cat.Stock(
                            warehouse_regions={"cpt": 5, "jhb": 2, "dbn": 1},
                            warehouses_total=7,
                            merchant=0,
                        ),
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
                    ),
                    "1332": cat.Offer(
                        id=1332,
                        availability=cat.Availability(status="buyable"),
                        condition="new",
                        stock=cat.Stock(
                            warehouse_regions={"cpt": 5, "jhb": 2, "dbn": 1},
                            warehouses_total=7,
                            merchant=0,
                        ),
                        pricing=cat.OfferPricing(
                            app=cat.OfferPrice(savings_percentage=11),
                            web=cat.OfferPrice(savings_percentage=22),
                        ),
                        promotions=[],
                    ),
                },
            )
        },
    )

    p = AdaptersFactory.from_productline_lineage(src)
    return CollectionsFactory.variants_from_productline_adapter(p)


@fixture()
def macbook_productline(macbook_productline_source):
    return AdaptersFactory.from_productline_lineage(macbook_productline_source)


@fixture()
def macbook_variants(macbook_productline):
    return CollectionsFactory.variants_from_productline_adapter(macbook_productline)


@fixture()
def macbook_offer(macbook_variants):
    return macbook_variants.find_offer_by_id(202151368)


@fixture()
def macbook_productline_preorder(macbook_productline_preorder_source):
    return AdaptersFactory.from_productline_lineage(macbook_productline_preorder_source)


@fixture()
def heavy_charge_macbook_productline(heavy_charge_macbook_productline_source):
    return AdaptersFactory.from_productline_lineage(
        heavy_charge_macbook_productline_source
    )


@fixture()
def macbook_productline_out_of_stock(macbook_productline_source_out_of_stock):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_source_out_of_stock
    )


@fixture()
def macbook_productline_disabled(macbook_productline_source_out_of_stock):
    source = copy.deepcopy(macbook_productline_source_out_of_stock)
    for variant in source["variants"].values():
        variant["variant"]["availability"]["status"] = "disabled"
        for offer in variant["offers"].values():
            offer["availability"]["status"] = "disabled"

    return AdaptersFactory.from_productline_lineage(source)


@fixture()
def macbook_productline_single_variant_multi_winner(
    macbook_productline_single_variant_multi_winner_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_single_variant_multi_winner_source
    )


@fixture()
def macbook_variants_single_variant_multi_winner(
    macbook_productline_single_variant_multi_winner,
):
    return CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_single_variant_multi_winner
    )


@fixture()
def macbook_productline_single_variant_single_winner(
    macbook_productline_single_variant_single_winner_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_single_variant_single_winner_source
    )


@fixture()
def macbook_productline_multi_variant_single_winner(
    macbook_productline_multi_variant_single_winner_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_multi_variant_single_winner_source
    )


@fixture()
def macbook_variants_single_variant_single_winner(
    macbook_productline_single_variant_single_winner,
):
    return CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_single_variant_single_winner
    )


@fixture()
def macbook_variants_multi_variant_single_winner(
    macbook_productline_multi_variant_single_winner,
):
    return CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_multi_variant_single_winner
    )


@fixture()
def macbook_productline_single_variant_used_winner(
    macbook_productline_single_variant_used_winner_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_single_variant_used_winner_source
    )


@fixture()
def macbook_variants_single_variant_used_winner(
    macbook_productline_single_variant_used_winner,
):
    return CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_single_variant_used_winner
    )


@fixture()
def macbook_productline_single_variant_out_of_stock(
    macbook_productline_single_variant_source_out_of_stock,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_single_variant_source_out_of_stock
    )


@fixture()
def macbook_variants_out_of_stock(
    macbook_productline_single_variant_out_of_stock,
):
    return CollectionsFactory.variants_from_productline_adapter(
        macbook_productline_single_variant_out_of_stock
    )


@fixture()
def macbook_productline_promotion_more_than_twenty(
    macbook_productline_promotion_more_than_twenty_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_promotion_more_than_twenty_source
    )


@fixture()
def macbook_productline_promotion_less_than_twenty(
    macbook_productline_promotion_less_than_twenty_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_promotion_less_than_twenty_source
    )


@fixture()
def macbook_offer_no_listing_price_difference(
    macbook_offer_no_listing_price_difference_source,
):
    return AdaptersFactory.from_offer_lineage(
        macbook_offer_no_listing_price_difference_source
    )


@fixture()
def macbook_productline_multibuy_one(
    macbook_productline_multibuy_one_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_multibuy_one_source
    )


@fixture()
def macbook_productline_multibuy_many(
    macbook_productline_multibuy_many_source,
):
    return AdaptersFactory.from_productline_lineage(
        macbook_productline_multibuy_many_source
    )
