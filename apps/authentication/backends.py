from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpRequest

User = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    """
    Custom authentication backend that permits users to authenticate
    using either their email address or phone number.
    """

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[User]:
        if username is None:
            username = kwargs.get("email") or kwargs.get("phone")

        if not username:
            return None

        try:
            # Query by email or phone
            user = User.objects.get(Q(email=username) | Q(phone=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
