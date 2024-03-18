from __future__ import annotations

from typing import TYPE_CHECKING, List

from storefront_product_adapter.models.buybox import BuyboxType

if TYPE_CHECKING:
    from storefront_product_adapter.adapters import (
        OfferAdapter,
        ProductlineAdapter,
        VariantAdapter,
    )
    from storefront_product_adapter.collections.variant import VariantCollection


class BuyboxPreferenceFacade:
    """
    This is a small facade to hold the logic for selecting a default buybox type
    preference (also known as offer preference outside of this library).

    It is expected to only be used when working with variants or productlines without
    a customer specified offer preference.
    """

    @staticmethod
    def get_default_for_variants(variants: VariantCollection) -> BuyboxType:
        """
        Currently all products in all cases will use lowest_priced as the default
        offer preference, so there is no real logic here. This should still be used,
        because it will make future business rule changes easier to handle if we
        need to do something more complicated.

        In the event of having to call other services to obtain information to be
        used for the rules here, this method will not be sufficient. At that point
        we will need to decide if we want to adopt an old pattern here of taking
        in callbacks.

        We ask for a variant collection parameter, but won't be using it (yet).
        """
        return BuyboxType.LOWEST_PRICED

    @staticmethod
    def get_default_for_productline(productline: ProductlineAdapter) -> BuyboxType:
        return BuyboxType.LOWEST_PRICED

    @staticmethod
    def get_default_for_variant(variant: VariantAdapter) -> BuyboxType:
        return BuyboxType.LOWEST_PRICED

    @staticmethod
    def get_default_for_offer(offer: OfferAdapter) -> BuyboxType:
        return BuyboxType.LOWEST_PRICED

    @staticmethod
    def get_display_preference_for_variants(
        variants: VariantCollection,
    ) -> List[BuyboxType]:
        """
        Primary usage will be to control the buybox types and order to be displayed
        on PDP when a variant is selected.

        The default buybox type (offer preference) will always be first so that
        the default type that is pre-selected is the first one.
        """

        preferences = [BuyboxPreferenceFacade.get_default_for_variants(variants)]

        for other in [BuyboxType.LOWEST_PRICED, BuyboxType.FASTEST]:
            if other not in preferences:
                preferences.append(other)

        return preferences
