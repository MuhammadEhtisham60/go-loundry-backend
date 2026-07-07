from typing import Optional, List
from django.contrib.auth import get_user_model
from apps.addresses.models import Address

User = get_user_model()


class AddressSelector:
    """
    Selectors encapsulating read queries for user saved addresses.
    """

    @staticmethod
    def get_user_addresses(user: User) -> List[Address]:
        """
        Retrieves all addresses saved by the user.
        """
        return list(Address.objects.filter(user=user))

    @staticmethod
    def get_default_address(user: User) -> Optional[Address]:
        """
        Retrieves the default address for the user, if set.
        """
        return Address.objects.filter(user=user, is_default=True).first()

    @staticmethod
    def get_address_by_id(user: User, address_id: str) -> Optional[Address]:
        """
        Retrieves a specific address by ID belonging to the user.
        """
        return Address.objects.filter(user=user, id=address_id).first()
