from django.db.models import QuerySet
from apps.services_catalog.models import Service


class CatalogSelector:
    """
    Selectors encapsulating read queries on the services catalog.
    Separates database queries from business mutations.
    """

    @staticmethod
    def get_active_services() -> QuerySet:
        """
        Returns all active services from the catalog ordered by display_order.
        """
        return Service.objects.active()

    @staticmethod
    def get_all_services(include_inactive: bool = True) -> QuerySet:
        """
        Returns all services, optionally including deactivated ones.
        """
        if include_inactive:
            return Service.objects.get_queryset()
        return Service.objects.active()
