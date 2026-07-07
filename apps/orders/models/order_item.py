import uuid
from django.db import models
from apps.orders.models.order import Order
from apps.services_catalog.models import Service


class OrderItem(models.Model):
    """
    Model linking services to specific laundry orders, capturing quantity
    and unit price at creation time.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"

    def __str__(self) -> str:
        return f"{self.service.name} x {self.quantity} (Order: {self.order_id})"
