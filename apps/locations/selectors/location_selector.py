from typing import List
from apps.locations.models import WarehouseSetting, DeliveryTier


class LocationSelector:
    """
    Selectors encapsulating database query logic for locations.
    """

    @staticmethod
    def get_warehouse_setting() -> WarehouseSetting:
        """
        Query and return the current Warehouse settings.
        """
        from apps.locations.services import LocationService

        return LocationService.get_or_default_warehouse()

    @staticmethod
    def list_delivery_tiers() -> List[DeliveryTier]:
        """
        Query and return all active delivery tiers ordered by minimum distance.
        """
        return list(DeliveryTier.objects.all())
