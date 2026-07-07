import uuid
from typing import Tuple, Dict
from django.db import models


class ServiceUnit(models.TextChoices):
    PIECE = "PIECE", "Per piece"
    KG = "KG", "Per KG"
    PAIR = "PAIR", "Per pair"
    SURCHARGE = "SURCHARGE", "Surcharge + base"


class ServiceQuerySet(models.QuerySet):
    def delete(self) -> int:
        # Bulk soft delete
        return self.update(is_deleted=True)


class ServiceManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        # Exclude deleted records by default
        return ServiceQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def active(self) -> models.QuerySet:
        return self.get_queryset().filter(is_active=True)


class Service(models.Model):
    """
    Model representing laundry services (e.g., Wash & Iron, Dry Cleaning).
    Supports soft deletion, active toggles, and catalog reordering.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit = models.CharField(
        max_length=20, choices=ServiceUnit.choices, default=ServiceUnit.PIECE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ServiceManager()
    all_objects = models.Manager()  # Direct manager to retrieve even soft-deleted records if needed

    class Meta:
        db_table = "services"
        ordering = ["display_order", "name"]

    def __str__(self) -> str:
        return f"{self.name} (Rs.{self.price} / {self.get_unit_display()})"

    def delete(self, *args, **kwargs) -> Tuple[int, Dict[str, int]]:
        # Single object soft delete
        self.is_deleted = True
        self.save()
        return 1, {self._meta.label: 1}
