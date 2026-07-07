from typing import Optional
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from apps.reviews.models import Review

User = get_user_model()


class ReviewSelector:
    """
    Selectors encapsulating read operations for customer ratings.
    """

    @staticmethod
    def get_reviews(
        user: Optional[User] = None,
        rating: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> QuerySet:
        """
        Retrieves reviews. For customers, isolates to their own.
        For admins, lists all with rating and date range filters.
        """
        queryset = Review.objects.select_related("user", "order")

        # Limit to own reviews for customer roles
        if user and user.role == "CUSTOMER":
            queryset = queryset.filter(user=user)

        if rating is not None:
            queryset = queryset.filter(rating=rating)

        if date_from and date_to:
            queryset = queryset.filter(created_at__date__range=[date_from, date_to])
        elif date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        elif date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset
