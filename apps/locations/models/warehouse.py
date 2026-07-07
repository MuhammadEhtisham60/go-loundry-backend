from django.db import models


class WarehouseSetting(models.Model):
    """
    Model storing settings for the GoLaundry central warehouse processing facility.
    Configurable coordinates and operational radius.
    """

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    max_service_radius_km = models.DecimalField(
        max_digits=5, decimal_places=2, default=15.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "warehouse_settings"

    def __str__(self) -> str:
        return f"Warehouse (Lat: {self.latitude}, Lon: {self.longitude}, Max Radius: {self.max_service_radius_km} KM)"
