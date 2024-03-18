from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from storefront_product_adapter.adapters.offer import OfferAdapter
from storefront_product_adapter.facades.pricing import PricingFacade
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition
from storefront_product_adapter.models.pricing import PriceRange

from storefront_api_views_product.errors import ViewConfigurationError

from .models import BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.adapters.productline import ProductlineAdapter
    from storefront_product_adapter.collections import VariantCollection
    from storefront_product_adapter.models.selectors import VariantSelectors


class EnhancedEcommerceListName(Enum):
    # For Search BFF
    SEARCH_RESULTS = "Search Results"
    DAILY_DEALS = "Daily Deals"
    ON_TAB = "On-tab Promos"

    # For Product BFF
    FREQUENTLY_BOUGHT_TOGETHER = "You Might Also Like"
    CUSTOMERS_ALSO_BOUGHT = "Customers Who Bought This Product, Also Bought"
    CART_RECOMMENDATIONS = "Cart Recommendations"
    CUSTOMER_RECOMMENDATIONS = "Recommended For You"
    TRENDING_RECOMMENDATIONS = "Trending"
    BESTSELLING_RECOMMENDATIONS = "Bestselling"
    WISHLIST_RECOMMENDATIONS = "Wishlist Trending"
    WISHLIST_PLIDS_RECOMMENDATIONS = "Wishlist With Products"
    FREE_DELIVERY_NUDGE = "Free Delivery Nudge"
    GENERIC_RECOMMENDATIONS = "Recommendations"
    MULTI_BUY = "Multi Buy"
    SET_BUNDLE = "Set Bundle"


CURRENCY_CODE = "ZAR"
MAX_NUM_CATEGORIES = 5


@dataclass
class EnhancedEcommerceProduct(BaseViewModel):
    """
    plid:
        Must be a string with "PLID" prefixed.
    name:
        Productline title.
    brand:
        Brand display value.
    category:
        Up to 5 items joined with `"/"`, no spaces.

        For PDP, this is a list of the display names of the productline's primary path.

        For Search, this is only populated when there is a category filter in the
        search request and that category ID is then used.
    variant:
        Colour name or None. Always None in search summary views.
    dimension1:
        Size name or None. Always None in search summary views.
    dimension2:
        Offer ID of the overall buybox winning offer.
        See `SummaryFacade.find_v1_offer_winners`.
        Note: For V2 we cannot pick an offer for out of stock productlines, where
        V1 would contain an implied/preferred offer at all times.
    price:
        Max price of winning offers, platform and context dependend.
        If there are no buyable offers, it will be based on the range of
        variant level selling_price fields. Uses PricingFacade.
        While Search is platform agnostic, PDP is not. There is also a special case
        where the app-only deals page shows search results with App prices.
    quantity:
        Mostly 1, but sometimes promotion qualifying quantity (bundles).
    position:
        Index in list of search results, starts from 0 on each page. Determined
        by the library user.
    """

    plid: str
    name: str
    brand: Optional[str]
    category: str
    variant: Optional[Any]
    dimension1: Optional[str]
    dimension2: Optional[int]
    price: int
    quantity: int
    position: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.plid,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "variant": self.variant,
            "dimension1": self.dimension1,
            "dimension2": self.dimension2,
            "price": self.price,
            "quantity": self.quantity,
            "position": self.position,
        }


@dataclass
class EnhancedEcommerceImpression(BaseViewModel):
    """
    This is nearly the same as `EnhancedEcommerceProduct`, but just different enough
    that inheriting isn't worth it. The same documentation applies to the fields that
    are in both.

    list_name:
        This field is dropped if None.
    """

    plid: str
    name: str
    list_name: Optional[EnhancedEcommerceListName]
    brand: Optional[str]
    category: str
    variant: Optional[Any]
    dimension1: Optional[str]
    dimension2: Optional[int]
    price: int
    position: int

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.plid,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "variant": self.variant,
            "dimension1": self.dimension1,
            "dimension2": self.dimension2,
            "price": self.price,
            "position": self.position,
        }

        if self.list_name is not None:
            data["list"] = self.list_name.value

        return data


@dataclass
class EcommerceActionField(BaseViewModel):
    list_name: Optional[EnhancedEcommerceListName]
    action: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """
        This unfortunate situation is one to revisit one day. For now, some users
        will want one or both fields.
        """
        data: Dict[str, Any] = {}

        if self.action is not None:
            data["action"] = self.action

        if self.list_name is not None:
            data["list"] = self.list_name.value

        return data


@dataclass
class EcommerceClick(BaseViewModel):
    products: List[EnhancedEcommerceProduct]
    action_field: EcommerceActionField
    currency_code: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "click": {
                "actionField": self.action_field.to_dict(),
                "products": [p.to_dict() for p in self.products],
            }
        }

        if self.currency_code is not None:
            data["currencyCode"] = self.currency_code

        return data


@dataclass
class EcommerceProducts(BaseViewModel):
    products: List[EnhancedEcommerceProduct]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "products": [p.to_dict() for p in self.products],
        }


@dataclass
class EcommerceAdd(BaseViewModel):
    add: EcommerceProducts
    currencyCode: str = CURRENCY_CODE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "currencyCode": self.currencyCode,
            "add": self.add.to_dict(),
        }


@dataclass
class EcommerceImpression(BaseViewModel):
    impressions: List[EnhancedEcommerceImpression]
    currencyCode: str = CURRENCY_CODE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "currencyCode": self.currencyCode,
            "impressions": [p.to_dict() for p in self.impressions],
        }


@dataclass
class EnhancedEcommerceClickView(BaseViewModel):
    ecommerce: EcommerceClick
    event: str

    def to_dict(self) -> Dict[str, Any]:
        return {"event": self.event, "ecommerce": self.ecommerce.to_dict()}


@dataclass
class EnhancedEcommerceAddToCartView(BaseViewModel):
    ecommerce: EcommerceAdd
    event: str

    def to_dict(self) -> Dict[str, Any]:
        return {"event": self.event, "ecommerce": self.ecommerce.to_dict()}


@dataclass
class EnhancedEcommerceImpressionView(BaseViewModel):
    ecommerce: EcommerceImpression
    event: str

    def to_dict(self) -> Dict[str, Any]:
        return {"event": self.event, "ecommerce": self.ecommerce.to_dict()}


def _build_eec_product(
    productline: ProductlineAdapter,
    offer_id: Optional[int],
    selectors: VariantSelectors,
    price_range: PriceRange,
    category_path: Optional[List[str]],
    quantity: int,
    position: int,
) -> EnhancedEcommerceProduct:
    category = ""
    if category_path:
        category = "/".join(category_path[:MAX_NUM_CATEGORIES])

    return EnhancedEcommerceProduct(
        plid=f"PLID{productline.productline_id}",
        name=productline.title,
        brand=productline.brand_name,
        category=category,
        variant=selectors.colour,
        dimension1=selectors.size,
        dimension2=offer_id,
        price=price_range.max,
        quantity=quantity,
        position=position,
    )


def _build_eec_impression(
    productline: ProductlineAdapter,
    offer_id: Optional[int],
    selectors: VariantSelectors,
    price_range: PriceRange,
    category_path: Optional[List[str]],
    list_name: Optional[EnhancedEcommerceListName],
    position: int,
) -> EnhancedEcommerceImpression:
    category = ""
    if category_path:
        category = "/".join(category_path[:MAX_NUM_CATEGORIES])

    return EnhancedEcommerceImpression(
        plid=f"PLID{productline.productline_id}",
        name=productline.title,
        list_name=list_name,
        brand=productline.brand_name,
        category=category,
        variant=selectors.colour,
        dimension1=selectors.size,
        dimension2=offer_id,
        price=price_range.max,
        position=position,
    )


class EnhancedEcommerceBaseViewFactory:
    def __init__(
        self,
        buybox_type: BuyboxType,
        enabled_variants: Optional[VariantCollection],
        offer: Optional[OfferAdapter],
        platform: Platform,
    ) -> None:
        """
        Parameters
        ----------
        enabled_variants:
            See BuyboxSummaryViewFactory
        offer:
            See BuyboxSummaryViewFactory
        platform:
            On PDP this should be the request platform.
            On Search this is almost always WEB. It should be APP when the results
            are for the app-only deals page, even when on desktop.
        """

        if offer is None and enabled_variants is not None:
            # New offers only
            pricing_collections = CollectionsFactory.pricing_from_variants(
                variants=enabled_variants,
                platform=platform,
                buybox_type=buybox_type,
                buybox_conditions_precedence=(OfferCondition.NEW,),
            )

            self.single_offer = pricing_collections.offers.get_singular()
            self.productline = enabled_variants.productline
            self.variant_selectors = (
                enabled_variants.get_selector_filter().to_variant_selectors()
            )

        elif offer is not None:
            # In this case, we're probably in Cart and need to verify what EEC
            # requirements they have on unboxed/used offers.
            pricing_collections = CollectionsFactory.pricing_from_offer(
                platform=platform, offer=offer
            )

            self.single_offer = offer
            self.productline = offer.variant.productline
            self.variant_selectors = offer.variant.get_applied_selector_names()
        else:
            raise ViewConfigurationError(
                "Either `enabled_variants` or `offer` must be given."
            )

        self.pricing = PricingFacade(pricing_collections)

    def _get_price_range(
        self,
    ) -> PriceRange:
        """
        All our views can build responses for disabled productlines, but for pricing
        then just leave fields empty or set to 0.
        So instead of raising an error, just populate what we can.

        Returns
        -------
            The displayable price range or an empty range (0 value).
        """
        price_range = self.pricing.get_display_price_range()
        if price_range is None:
            return PriceRange()
        return price_range


class EnhancedEcommerceClickViewFactory(EnhancedEcommerceBaseViewFactory):
    def __init__(
        self,
        buybox_type: BuyboxType,
        enabled_variants: Optional[VariantCollection],
        offer: Optional[OfferAdapter],
        platform: Platform,
        event: str = "eec.productClick",
        include_currency: bool = False,  # Default favours Summary views
        include_action: bool = True,  # Default favours Summary views
    ) -> None:
        """
        Parameters
        ----------
        productline:
            Productline
        variants:
            Collection of buyable and non_buyable variants from `productline`.
        offers:
            Buybox winners to consider for price range.
        platform:
            On PDP this should be the request platform.
            On Search this is almost always WEB. It should be APP when the results
            are for the app-only deals page, even when on desktop.
        """
        super().__init__(
            buybox_type=buybox_type,
            enabled_variants=enabled_variants,
            offer=offer,
            platform=platform,
        )
        self.event = event
        self.include_currency = include_currency
        self.include_action = include_action

    def build(
        self,
        list_name: Optional[EnhancedEcommerceListName],
        category_path: Optional[List[str]],
        position: int,
        quantity: int = 1,
        price_override: Optional[int] = None,
    ) -> EnhancedEcommerceClickView:
        """Build this ecommerce view.

        Parameters
        ----------
        list_name:
            Depends on context.
        category_path:
            A list of display names, starting with department followed by up to 4
            categories. If more categories are present, they are ignored.

            For PDP, this must be obtained productline's primary path.

            For Search, this is only populated when there is a category filter in the
            search request and that category ID is then used. The library user
            needs to obtain the category path.
        position:
            Directly assigned to the `position` field. This usually matches the
            position in a search result page.
        quantity:
            This is almost always 1, except for certain bundle deal items which
            the caller will need to set.
        price_override:
            For things like bundle deals, the caller will have a promotional price
            that needs to be used here instead of the price range value.
        """

        if price_override:
            price_range = PriceRange(min=price_override, max=price_override)
        else:
            price_range = self._get_price_range()

        item = _build_eec_product(
            productline=self.productline,
            offer_id=self.single_offer.offer_id if self.single_offer else None,
            selectors=self.variant_selectors,
            price_range=price_range,
            category_path=category_path,
            quantity=quantity,
            position=position,
        )

        if self.include_action:
            action_field = EcommerceActionField(action="click", list_name=list_name)
        else:
            action_field = EcommerceActionField(action=None, list_name=list_name)

        currency_code = None
        if self.include_currency:
            currency_code = CURRENCY_CODE

        return EnhancedEcommerceClickView(
            event=self.event,
            ecommerce=EcommerceClick(
                action_field=action_field,
                currency_code=currency_code,
                products=[item],
            ),
        )


class EnhancedEcommerceAddToCartViewFactory(EnhancedEcommerceBaseViewFactory):
    def __init__(
        self,
        buybox_type: BuyboxType,
        enabled_variants: Optional[VariantCollection],
        offer: Optional[OfferAdapter],
        platform: Platform,
        event: str = "eec.addToCart",
    ) -> None:
        """
        Parameters
        ----------
        productline:
            Productline
        variants:
            Collection of buyable and non_buyable variants from `productline`.
        offers:
            Buybox winners to consider for price range.
        platform:
            On PDP this should be the request platform.
            On Search this is almost always WEB. It should be APP when the results
            are for the app-only deals page, even when on desktop.
        event:
            The string to use for the `event` field.
        """
        super().__init__(
            buybox_type=buybox_type,
            enabled_variants=enabled_variants,
            offer=offer,
            platform=platform,
        )
        self.event = event

    def build(
        self,
        category_path: Optional[List[str]],
        position: int,
        quantity: int = 1,
        price_override: Optional[int] = None,
    ) -> EnhancedEcommerceAddToCartView:
        """Build this ecommerce view.

        Parameters
        ----------
        category_path:
            A list of display names, starting with department followed by up to 4
            categories. If more categories are present, they are ignored.

            For PDP, this must be obtained productline's primary path.

            For Search, this is only populated when there is a category filter in the
            search request and that category ID is then used. The library user
            needs to obtain the category path.
        position:
            Directly assigned to the `position` field. This usually matches the
            position in a search result page.
        quantity:
            This is almost always 1, except for certain bundle deal items which
            the caller will need to set.
        price_override:
            For things like bundle deals, the caller will have a promotional price
            that needs to be used here instead of the price range value.
        """

        if price_override:
            price_range = PriceRange(min=price_override, max=price_override)
        else:
            price_range = self._get_price_range()

        item = _build_eec_product(
            productline=self.productline,
            offer_id=self.single_offer.offer_id if self.single_offer else None,
            selectors=self.variant_selectors,
            price_range=price_range,
            category_path=category_path,
            quantity=quantity,
            position=position,
        )

        return EnhancedEcommerceAddToCartView(
            event=self.event,
            ecommerce=EcommerceAdd(add=EcommerceProducts(products=[item])),
        )

    @classmethod
    def build_empty(
        cls, event: str = "eec.addToCart"
    ) -> EnhancedEcommerceAddToCartView:
        return EnhancedEcommerceAddToCartView(
            event=event,
            ecommerce=EcommerceAdd(add=EcommerceProducts(products=[])),
        )

    @classmethod
    def merge_list(
        cls,
        views: List[EnhancedEcommerceAddToCartView],
        position_offset: Optional[int] = None,
    ) -> EnhancedEcommerceAddToCartView:
        """
        In some contexts the final view does not contain multiple instances of this view
        with a single product, but instead a single view with multiple products. Such a
        caller will still need to build each item with varying parameters separately in
        some form. Rather than pre-building a large list and passing that to this
        factory, keep the interface simple and provide this merge method as a last step
        the caller can use to repackage the view.

        Alternatives:
        1. Keep state in the factory. Initialise with minimal parameters, then
           add one new item at a time from either variants or offer. Finally call
           the build method to build what the current state is. Then what? Clear,
           don't care, lock?
        2. Take lists of inputs. This is tricky when you need to either take in a list
           of variant collections or a list of offers. If we do this, we first make
           very sure of what we are actually trying to build.

        Parameters
        ----------
        position_offset:
            If this is None, this method will NOT modify any `position` values.
            If it has any integer value, it will be used as the first position value
            and each subsequent item's position will be incremented by one.
        """
        merged = EnhancedEcommerceAddToCartViewFactory.build_empty(event=views[0].event)

        for v in views:
            merged.ecommerce.add.products.extend(v.ecommerce.add.products)

        if position_offset is not None:
            for idx, product in enumerate(merged.ecommerce.add.products):
                product.position = position_offset + idx

        return merged


class EnhancedEcommerceImpressionViewFactory(EnhancedEcommerceBaseViewFactory):
    def __init__(
        self,
        buybox_type: BuyboxType,
        enabled_variants: Optional[VariantCollection],
        offer: Optional[OfferAdapter],
        platform: Platform,
        event: str = "eec.productImpressions",
    ) -> None:
        """
        Parameters
        ----------
        productline:
            Productline
        variants:
            Collection of buyable and non_buyable variants from `productline`.
        offers:
            Buybox winners to consider for price range.
        platform:
            On PDP this should be the request platform.
            On Search this is almost always WEB. It should be APP when the results
            are for the app-only deals page, even when on desktop.
        """
        super().__init__(
            buybox_type=buybox_type,
            enabled_variants=enabled_variants,
            offer=offer,
            platform=platform,
        )
        self.event = event

    def build(
        self,
        list_name: Optional[EnhancedEcommerceListName],
        category_path: Optional[List[str]],
        position: int,
        price_override: Optional[int] = None,
    ) -> EnhancedEcommerceImpressionView:
        """Build this ecommerce view.

        Parameters
        ----------
        list_name
            Depends on context.
        category_path:
            A list of display names, starting with department followed by up to 4
            categories. If more categories are present, they are ignored.

            For PDP, this must be obtained productline's primary path.

            For Search, this is only populated when there is a category filter in the
            search request and that category ID is then used. The library user
            needs to obtain the category path.
        position:
            Directly assigned to the `position` field. This usually matches the
            position in a search result page.
        price_override:
            For things like bundle deals, the caller will have a promotional price
            that needs to be used here instead of the price range value.
        """

        if price_override:
            price_range = PriceRange(min=price_override, max=price_override)
        else:
            price_range = self._get_price_range()

        item = _build_eec_impression(
            productline=self.productline,
            offer_id=self.single_offer.offer_id if self.single_offer else None,
            selectors=self.variant_selectors,
            price_range=price_range,
            category_path=category_path,
            position=position,
            list_name=list_name,
        )

        return EnhancedEcommerceImpressionView(
            event=self.event, ecommerce=EcommerceImpression(impressions=[item])
        )

    @classmethod
    def build_empty(
        cls, event: str = "eec.productImpressions"
    ) -> EnhancedEcommerceImpressionView:
        return EnhancedEcommerceImpressionView(
            event=event,
            ecommerce=EcommerceImpression(impressions=[]),
        )

    @classmethod
    def merge_list(
        cls,
        views: List[EnhancedEcommerceImpressionView],
        position_offset: Optional[int] = None,
    ) -> EnhancedEcommerceImpressionView:
        """
        See `EnhancedEcommerceAddToCartView.merge_list`
        """

        merged = EnhancedEcommerceImpressionViewFactory.build_empty(
            event=views[0].event
        )

        for v in views:
            merged.ecommerce.impressions.extend(v.ecommerce.impressions)

        if position_offset is not None:
            for idx, impression in enumerate(merged.ecommerce.impressions):
                impression.position = position_offset + idx

        return merged
