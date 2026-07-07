from decimal import Decimal
from typing import Tuple, Dict, Any
from rest_framework import serializers

from apps.locations.models import WarehouseSetting, DeliveryTier
from apps.common.services.maps import MapsService


class LocationService:
    """
    Service layer handling warehouse configuration management,
    client area eligibility checks, and tier-based delivery fee calculations.
    """

    @staticmethod
    def get_or_default_warehouse() -> WarehouseSetting:
        """
        Retrieves the singleton warehouse settings record.
        Creates a default record if none exists ( Karachi Clifton coordinates fallback ).
        """
        warehouse = WarehouseSetting.objects.first()
        if not warehouse:
            warehouse = WarehouseSetting.objects.create(
                latitude=Decimal("24.8138"),
                longitude=Decimal("67.0336"),
                max_service_radius_km=Decimal("15.00"),
            )
        return warehouse

    @staticmethod
    def update_warehouse(latitude: Decimal, longitude: Decimal, radius_km: Decimal) -> WarehouseSetting:
        """
        Updates the warehouse coordinates and maximum operational range.
        """
        warehouse = LocationService.get_or_default_warehouse()
        warehouse.latitude = latitude
        warehouse.longitude = longitude
        warehouse.max_service_radius_km = radius_km
        warehouse.save()
        return warehouse

    @staticmethod
    def get_delivery_charge(distance_km: float) -> Decimal:
        """
        Determines the delivery fee based on distance from the warehouse
        matching the configured DeliveryTiers.
        """
        dist_dec = Decimal(str(distance_km))
        # Find matching tier
        tier = DeliveryTier.objects.filter(
            min_distance_km__lte=dist_dec, max_distance_km__gt=dist_dec
        ).first()

        if tier:
            return tier.charge

        # Fallback default if tiers are empty:
        # 0 - 5 km = 0, 5 - 10 km = 100, 10 - 15 km = 200
        if dist_dec <= Decimal("5.0"):
            return Decimal("0.00")
        elif dist_dec <= Decimal("10.0"):
            return Decimal("100.00")
        elif dist_dec <= Decimal("15.0"):
            return Decimal("200.00")

        return Decimal("300.00")  # Default out of tier range surcharge

    @staticmethod
    def validate_service_area(latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Calculates distance from client address to warehouse,
        verifying if it's within radius bounds, and calculates delivery fees.
        """
        warehouse = LocationService.get_or_default_warehouse()
        distance = MapsService.calculate_distance(
            latitude, longitude, warehouse.latitude, warehouse.longitude
        )

        is_valid = Decimal(str(distance)) <= warehouse.max_service_radius_km
        charge = LocationService.get_delivery_charge(distance) if is_valid else Decimal("0.00")

        return {
            "is_valid": is_valid,
            "distance_km": distance,
            "delivery_charge": charge,
            "warehouse_latitude": warehouse.latitude,
            "warehouse_longitude": warehouse.longitude,
            "max_service_radius_km": warehouse.max_service_radius_km,
        }
