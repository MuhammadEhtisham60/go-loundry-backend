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
                address="Lahore Central Warehouse",
            )
        return warehouse

    @staticmethod
    def update_warehouse(
        latitude: Decimal, longitude: Decimal, radius_km: Decimal, address: str = ""
    ) -> WarehouseSetting:
        """
        Updates the warehouse coordinates, address, and maximum operational range.
        """
        warehouse = LocationService.get_or_default_warehouse()
        warehouse.latitude = latitude
        warehouse.longitude = longitude
        warehouse.max_service_radius_km = radius_km
        warehouse.address = address
        warehouse.save()
        return warehouse

    @staticmethod
    def bulk_update_tiers(tiers_data: list) -> list:
        """
        Atomically deletes all existing delivery tiers and replaces them with new ones.
        """
        from django.db import transaction
        with transaction.atomic():
            DeliveryTier.objects.all().delete()
            created_tiers = []
            for item in tiers_data:
                tier = DeliveryTier.objects.create(
                    min_distance_km=item["min_distance_km"],
                    max_distance_km=item["max_distance_km"],
                    charge=item["charge"],
                )
                created_tiers.append(tier)
            return created_tiers

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
        Calculates distance from client address to closest warehouse,
        verifying if it's within radius bounds, and calculates delivery fees.
        """
        warehouses = WarehouseSetting.objects.all()
        if not warehouses.exists():
            # Fallback default if none exist
            warehouse = LocationService.get_or_default_warehouse()
            warehouses = [warehouse]

        best_warehouse = None
        min_distance = float('inf')

        for w in warehouses:
            dist = MapsService.calculate_distance(
                latitude, longitude, w.latitude, w.longitude
            )
            if dist < min_distance:
                min_distance = dist
                best_warehouse = w

        is_valid = Decimal(str(min_distance)) <= best_warehouse.max_service_radius_km
        charge = LocationService.get_delivery_charge(min_distance) if is_valid else Decimal("0.00")

        return {
            "is_valid": is_valid,
            "distance_km": min_distance,
            "delivery_charge": charge,
            "warehouse_latitude": best_warehouse.latitude,
            "warehouse_longitude": best_warehouse.longitude,
            "warehouse_address": best_warehouse.address,
            "max_service_radius_km": best_warehouse.max_service_radius_km,
        }
