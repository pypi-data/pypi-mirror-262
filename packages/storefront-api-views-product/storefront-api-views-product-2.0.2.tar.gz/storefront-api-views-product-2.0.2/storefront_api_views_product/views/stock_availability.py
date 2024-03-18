from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Collection, Dict, List, Optional, Tuple

from storefront_product_adapter.collections import VariantCollection
from storefront_product_adapter.factories.collections import CollectionsFactory
from storefront_product_adapter.models.buybox import BuyboxType
from storefront_product_adapter.models.common import Platform
from storefront_product_adapter.models.condition import OfferCondition
from storefront_product_adapter.models.stock import OfferStockStatus, StockQuantity
from storefront_product_adapter.utils.datetime import DateTimeUtils

from .models import BaseViewModel

if TYPE_CHECKING:
    from storefront_product_adapter.adapters.offer import OfferAdapter


@dataclass
class InternalDistributionCentre:
    text: str
    description: str
    info_mode: str
    long_name: str


@dataclass
class DistributionCentre(BaseViewModel):
    distribution_centre_id: str
    text: str
    description: str
    info_mode: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.distribution_centre_id,
            "text": self.text,
            "info_mode": self.info_mode,
            "description": self.description,
        }


class RegionMapping:
    _regions_lookup = {
        "cpt": "Cape Town",
        "dbn": "Durban",
        "jhb": "Johannesburg",
    }

    @classmethod
    def get_name_from_code(cls, region_code: str) -> str:
        return cls._regions_lookup.get(region_code, region_code.upper())


@dataclass
class StockAvailabilitySummaryView(BaseViewModel):
    """
    is_displayed:
        Field for Offer Optimisation transition. Before Offer Optimisation this
        will be set to None and omitted from the model output.
        After Offer Optimisation it will be set to False and included. Frontends
        will then look for the field and honour it. Currently we do not expect
        to set this to True, but we need it to control Offer Optimisation transition
        and while we have it we may one day decide to enable it.

    is_imported:
        Legacy field, should always be False.
    """

    status: str
    is_leadtime: bool
    distribution_centres: List[DistributionCentre]
    is_displayed: Optional[bool]
    is_imported: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "status": self.status,
            "is_leadtime": self.is_leadtime,
            "is_imported": self.is_imported,
            "distribution_centres": [
                dc.to_dict() for dc in self.distribution_centres if dc
            ],
        }

        if self.is_displayed is not None:
            data["is_displayed"] = self.is_displayed

        return data


class StockAvailabilitySummaryViewFactory:
    def __init__(
        self,
        *,
        buybox_type: BuyboxType,
        enabled_variants: Optional[VariantCollection],
        specific_offer: Optional[OfferAdapter],
    ) -> None:
        """
        Stock availability before OfferOpt is only ever shown on search results
        when there is an add-to-cart offer available or it is non_buyable.

        Also TODO: DSC-7364 - fancy future pre-order text.

        Parameters
        ----------
        buybox_type
            Buybox type to build the view with. Mainly being used to determine if we
            need to use old `custom_1` rules or new multi-winner rules.
        enabled_variants
            In a search context this should be provided and will override the specific
            offer status if there is more than one buyable variant.
            In a cart context this can be None, assuming that a specific offer is given.
        specific_offer
            When enabled_variants is None, this will be used
            to determine stock availability summary view information.
            In a search context this will be the overall buybox winner - should be
            the cheapest buyable offer across all variants (for a buybox type
            determined by offer optimisation status).
            In a cart context, this is simply the specific offer that is in the cart -
            no other criteria applies.
        """
        self._buybox_type = buybox_type
        self._enabled_variants = enabled_variants
        self._specific_offer = specific_offer

        self._winning_buybox_types: Collection[BuyboxType]
        if self._buybox_type == BuyboxType.CUSTOM_1:
            self._winning_buybox_types = (BuyboxType.CUSTOM_1,)
        else:
            # We are in OfferOpt mode and need to get the winners from all OfferOpt
            # buybox type winners.
            self._winning_buybox_types = (BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST)

    def build(self, is_displayed: Optional[bool]) -> StockAvailabilitySummaryView:
        """
        Parameters
        ----------
        is_displayed:
            If set to True or False, a field called `is_displayed` will be included
            in the view with this value.
            If None, the field is omitted.
            It will only be used in the case where the library deems stock info
            to be available in the first place. This excludes variants and multi-winner
            items.
        """

        if self._enabled_variants is not None:
            return self._build_variants(
                enabled_variants=self._enabled_variants, is_displayed=is_displayed
            )

        if self._specific_offer is not None:
            return self._build_offer(
                offer=self._specific_offer, is_displayed=is_displayed
            )

        # We weren't given anything to build with, so return empty stuff
        if is_displayed:
            # Only flip this if it was expecting to do something, so keep None
            is_displayed = False

        return StockAvailabilitySummaryView(
            is_leadtime=False,
            status="",
            distribution_centres=[],
            is_displayed=is_displayed,
        )

    def _build_variants(
        self, enabled_variants: VariantCollection, is_displayed: Optional[bool]
    ) -> StockAvailabilitySummaryView:
        # Caller specifically provided variants and we can now see if there are
        # multiple buybox winners in which case we hide the stock info.
        # We mainly expect search context to pass a collection here, cart will only
        # work with offer level and should not need to make a variant collection.

        only_offer = None
        winner_by_platform = {}
        all_variants_out_of_stock = True
        for platform in (Platform.WEB, Platform.APP):
            all_winners = CollectionsFactory.offer_winners_for_buyboxes(
                platform=platform,
                variants=enabled_variants,
                buybox_types=self._winning_buybox_types,
                buybox_conditions_precedence=(
                    OfferCondition.NEW,
                    OfferCondition.USED,
                ),
            )
            if not all_winners.is_empty():
                all_variants_out_of_stock = False
            winner_by_platform[platform] = all_winners.get_singular()

        if winner_by_platform[Platform.WEB] == winner_by_platform[Platform.APP]:
            # All platforms have the same single winner, so we can reliably
            # display the stock status for this winner.
            only_offer = next(iter(winner_by_platform.values()))

        # No matter what happened above, it this is a multi-variant item
        # we don't want to show stock info if only one of its variants are
        # buyable - still let the user go to PDP to see choices.
        if len(enabled_variants) > 1:
            only_offer = None

        if only_offer is None:
            if all_variants_out_of_stock:
                # No buyable variants and we were given a variant collection.
                # Whether disabled or out of stock, show the same text.
                stock_text = "Supplier out of stock"
            else:
                # Either all offers disabled or more than one buyable, same result
                # for here: No stock status to display.
                if is_displayed:
                    # Only flip the flag if it was given. If it was None, keep it None
                    is_displayed = False
                stock_text = ""
            return StockAvailabilitySummaryView(
                is_leadtime=False,
                status=stock_text,
                distribution_centres=[],
                is_displayed=is_displayed,
            )

        return self._build_offer(only_offer, is_displayed)

    def _build_offer(
        self, offer: OfferAdapter, is_displayed: Optional[bool]
    ) -> StockAvailabilitySummaryView:
        internal_dcs: list[InternalDistributionCentre]
        distribution_centres: list[DistributionCentre]

        stock_status, stock_text = self._get_availability_status(offer=offer)
        stock_qtys = offer.get_stock_quantities()

        internal_dcs = self._build_distribution_centres(
            stock_qtys=stock_qtys,
        )

        distribution_centres = [
            DistributionCentre(
                distribution_centre_id=f"distribution-centre-{index}",
                text=dc.text,
                info_mode=dc.info_mode,
                description=f"This item can be shipped from {dc.long_name}.",
            )
            for index, dc in enumerate(internal_dcs)
        ]

        return StockAvailabilitySummaryView(
            is_leadtime=(stock_status == OfferStockStatus.LEAD_TIME),
            status=stock_text,
            distribution_centres=distribution_centres,
            is_displayed=is_displayed,
        )

    def _get_availability_status(
        self, offer: OfferAdapter
    ) -> Tuple[OfferStockStatus, str]:
        stock_status = offer.get_stock_status()
        released_date = offer.variant.productline.timestamp_released

        if stock_status == OfferStockStatus.IN_STOCK:
            if offer.is_unboxed_offer():
                return (stock_status, "Unboxed stock available")
            if offer.variant.productline.is_digital():
                return (stock_status, "Available now")
            return (stock_status, "In stock")
        elif stock_status == OfferStockStatus.LEAD_TIME:
            lead_times = offer.get_leadtimes()
            text = f"Ships in {lead_times.min_days} - {lead_times.max_days} work days"
            return (stock_status, text)

        # Check if item is available for Pre-order
        if released_date and stock_status == OfferStockStatus.PRE_ORDER_LIVE:
            day_str = DateTimeUtils.format_preorder_day(released_date)
            return (stock_status, f"Pre-order: Ships {day_str}")

        # Realistically we should not get to this point in normal operation, but
        # in case we have any state that we don't handle, just make sure it has
        # a sensible value
        return (OfferStockStatus.OUT_OF_STOCK, "Supplier out of stock")

    def _build_distribution_centres(
        self, stock_qtys: StockQuantity
    ) -> List[InternalDistributionCentre]:
        result: List[InternalDistributionCentre] = []

        for region_code, quantity in sorted(stock_qtys.warehouse_regions.items()):
            if quantity > 0:
                region_text = region_code.upper()
                region_name = RegionMapping.get_name_from_code(region_code)
                description = f"This item can be shipped from {region_name}."
                result.append(
                    InternalDistributionCentre(
                        text=region_text,
                        long_name=region_name,
                        description=description,
                        info_mode="short",
                    )
                )

        return result
