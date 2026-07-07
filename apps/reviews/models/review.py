import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.orders.models import Order

User = get_user_model()


class Review(models.Model):
    """
    Model representing user ratings and remarks for specific laundry orders.
    Constraints: 1-to-1 linkage to Order, rating validation between 1 and 5.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="review")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    remarks = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Review (Order: {self.order_id}, Rating: {self.rating})"
