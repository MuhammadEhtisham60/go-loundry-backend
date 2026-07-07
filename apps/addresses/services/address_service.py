from typing import Dict, Any
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from apps.addresses.models import Address

User = get_user_model()


class AddressService:
    """
    Service layer containing operations for modifying saved customer addresses.
    Includes ensuring only one default address exists per customer.
    """

    @staticmethod
    def create_address(user: User, validated_data: Dict[str, Any]) -> Address:
        """
        Creates a new address for a user.
        Clears default flag on other user addresses if is_default=True.
        """
        is_default = validated_data.get("is_default", False)

        with transaction.atomic():
            if is_default:
                Address.objects.filter(user=user).update(is_default=False)
            
            # If this is the user's first address, make it default automatically
            if not Address.objects.filter(user=user).exists():
                validated_data["is_default"] = True

            address = Address.objects.create(user=user, **validated_data)
            return address

    @staticmethod
    def update_address(
        user: User, address_id: str, validated_data: Dict[str, Any]
    ) -> Address:
        """
        Updates an existing address.
        Clears default flag on other user addresses if updated is_default=True.
        """
        address = get_object_or_404(Address, id=address_id, user=user)
        is_default = validated_data.get("is_default", False)

        with transaction.atomic():
            if is_default:
                Address.objects.filter(user=user).update(is_default=False)

            for key, value in validated_data.items():
                setattr(address, key, value)
            address.save()
            return address

    @staticmethod
    def delete_address(user: User, address_id: str) -> None:
        """
        Deletes a customer's saved address.
        If deleted address was default, marks the remaining newest address as default.
        """
        address = get_object_or_404(Address, id=address_id, user=user)
        was_default = address.is_default

        with transaction.atomic():
            address.delete()
            if was_default:
                next_addr = Address.objects.filter(user=user).order_by("-created_at").first()
                if next_addr:
                    next_addr.is_default = True
                    next_addr.save()
