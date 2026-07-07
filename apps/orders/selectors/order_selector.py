from typing import Optional, List
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from apps.orders.models import Order

User = get_user_model()


class OrderSelector:
    """
    Selectors for handling orders retrieval, listing, and filtering.
    Optimizes queries using select_related and prefetch_related.
    """

    @staticmethod
    def get_order_by_id(order_id: str, user: Optional[User] = None) -> Optional[Order]:
        """
        Retrieves a single order by ID, optionally validating ownership for customers.
        """
        queryset = Order.objects.select_related("user", "pickup_address").prefetch_related("items__service")
        
        if user and user.role == "CUSTOMER":
            return queryset.filter(id=order_id, user=user).first()
            
        return queryset.filter(id=order_id).first()

    @staticmethod
    def list_orders(
        user: User,
        status_value: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> QuerySet:
        """
        Queries orders lists. For customers, isolates to their own.
        For admins/support agents, list all with search and filter queries.
        """
        queryset = Order.objects.select_related("user").prefetch_related("items__service")

        # Role checks
        if user.role == "CUSTOMER":
            queryset = queryset.filter(user=user)
        else:
            if customer_id:
                queryset = queryset.filter(user_id=customer_id)

        # Filters
        if status_value:
            queryset = queryset.filter(status=status_value)

        if date_from and date_to:
            queryset = queryset.filter(created_at__date__range=[date_from, date_to])
        elif date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        elif date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset
