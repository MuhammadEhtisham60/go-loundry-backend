import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.addresses.models import Address

User = get_user_model()


class OrderStatus(models.TextChoices):
    ORDER_PLACED = "ORDER_PLACED", "Order Placed"
    ORDER_CONFIRMED = "ORDER_CONFIRMED", "Order Confirmed"
    PICKUP_SCHEDULED = "PICKUP_SCHEDULED", "Pickup Scheduled"
    PICKED_UP = "PICKED_UP", "Picked Up"
    IN_PROCESS = "IN_PROCESS", "In Process"
    READY_FOR_DELIVERY = "READY_FOR_DELIVERY", "Ready for Delivery"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "CANCELLED", "Cancelled"


class PickupSlot(models.TextChoices):
    MORNING = "MORNING", "Morning"
    AFTERNOON = "AFTERNOON", "Afternoon"
    EVENING = "EVENING", "Evening"


class PaymentMethod(models.TextChoices):
    COD = "COD", "Cash on Delivery"


class Order(models.Model):
    """
    Model representing customer laundry orders, capture prices, address coordinate backups,
    tracking statuses, slot timings, and assigned riders.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(
        max_length=30, choices=OrderStatus.choices, default=OrderStatus.ORDER_PLACED
    )

    # Address snapshot to prevent details loss if user updates their profile address list
    pickup_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    address_line_snapshot = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Calculations
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_services_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Timings
    pickup_date = models.DateField()
    pickup_slot = models.CharField(
        max_length=20, choices=PickupSlot.choices, default=PickupSlot.MORNING
    )
    special_instructions = models.TextField(blank=True, default="")

    # Payment details
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.COD
    )

    # Back office assignees
    rider_name = models.CharField(max_length=255, null=True, blank=True)
    rider_contact = models.CharField(max_length=50, null=True, blank=True)
    admin_notes = models.TextField(null=True, blank=True)
    cancellation_reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.id} - Status: {self.get_status_display()}"
