from typing import Dict, Any, List
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.services_catalog.models import Service


class CatalogService:
    """
    Service layer for managing the laundry services catalog.
    Handles service creation, modification, deletion, and sequence reordering.
    """

    @staticmethod
    def create_service(validated_data: Dict[str, Any]) -> Service:
        """
        Creates and saves a new Service in the catalog.
        """
        return Service.objects.create(**validated_data)

    @staticmethod
    def update_service(service_id: str, validated_data: Dict[str, Any]) -> Service:
        """
        Updates an existing Service.
        """
        service = get_object_or_404(Service, id=service_id)
        for key, value in validated_data.items():
            setattr(service, key, value)
        service.save()
        return service

    @staticmethod
    def soft_delete_service(service_id: str) -> None:
        """
        Soft deletes a service from the catalog.
        """
        service = get_object_or_404(Service, id=service_id)
        service.delete()

    @staticmethod
    def reorder_services(reorder_list: List[Dict[str, Any]]) -> None:
        """
        Updates the display sequences in bulk.
        Ensures updates are transactionally safe.
        """
        with transaction.atomic():
            for item in reorder_list:
                service_id = item.get("id")
                display_order = item.get("display_order")
                if service_id is not None and display_order is not None:
                    Service.objects.filter(id=service_id).update(
                        display_order=display_order
                    )
