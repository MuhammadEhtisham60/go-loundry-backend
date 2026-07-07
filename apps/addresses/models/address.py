import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AddressType(models.TextChoices):
    HOME = "HOME", "Home"
    OFFICE = "OFFICE", "Office"
    OTHER = "OTHER", "Other"


class Address(models.Model):
    """
    Model storing customer's physical addresses alongside geographic coordinate pins.
    Used for verifying location and mapping delivery fees.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(
        max_length=20, choices=AddressType.choices, default=AddressType.HOME
    )
    address_line = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addresses"
        ordering = ["-is_default", "-created_at"]

    def __str__(self) -> str:
        return f"{self.user.email or self.user.phone} - {self.get_address_type_display()} ({self.address_line[:30]})"
