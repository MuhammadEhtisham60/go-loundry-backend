from django.db import models


class DeliveryTier(models.Model):
    """
    Model storing dynamic delivery charge tiers based on distance intervals from the warehouse.
    Example: 0 - 5 KM = Free, 5 - 10 KM = Rs.100, 10 - 15 KM = Rs.200
    """

    min_distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    max_distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "delivery_tiers"
        ordering = ["min_distance_km"]

    def __str__(self) -> str:
        return f"{self.min_distance_km} to {self.max_distance_km} KM: Rs.{self.charge}"
