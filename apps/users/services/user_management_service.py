from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class UserManagementService:
    """
    Service layer containing operations for administrator customer management.
    """

    @staticmethod
    def set_block_status(user_id: str, is_blocked: bool) -> User:
        """
        Updates the block status for a customer.
        """
        user = get_object_or_404(User, id=user_id)
        user.is_blocked = is_blocked
        user.save()
        return user
