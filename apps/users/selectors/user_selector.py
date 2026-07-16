from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from apps.authentication.models.user import UserRole, UserType

User = get_user_model()


class UserSelector:
    """
    Selectors encapsulating read operations for customer queries.
    """

    @staticmethod
    def get_customers(
        search_query: str = None, is_blocked: bool = None
    ) -> QuerySet:
        """
        Query and return a list of registered customers.
        Supports searching on email, phone, and name.
        """
        queryset = User.objects.filter(
            Q(role=UserRole.CUSTOMER) | Q(user_type=UserType.USER)
        ).exclude(
            role__in=[UserRole.SUPPORT_AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]
        )

        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query)
                | Q(phone__icontains=search_query)
                | Q(full_name__icontains=search_query)
            )

        if is_blocked is not None:
            queryset = queryset.filter(is_blocked=is_blocked)

        return queryset

    @staticmethod
    def get_customer_by_id(customer_id: str) -> User:
        """
        Query and return a single customer by their ID.
        """
        return User.objects.filter(
            Q(id=customer_id),
            Q(role=UserRole.CUSTOMER) | Q(user_type=UserType.USER)
        ).exclude(
            role__in=[UserRole.SUPPORT_AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]
        ).first()

