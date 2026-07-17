from rest_framework import permissions
from apps.authentication.permissions import IsAdmin, IsSupportAgent


class HasPermissionCode(permissions.BasePermission):
    """
    Custom permission class verifying if a user's role contains the required permission code.
    Super Admin bypasses all checks.
    """

    def __init__(self, required_code: str = "users"):
        self.required_code = required_code

    def __call__(self) -> "HasPermissionCode":
        return self

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Super Admin bypasses all permission code checks
        if request.user.is_superuser:
            return True
        if getattr(request.user, "user_type", None) == "super_admin":
            return True
        if request.user.role and request.user.role.name == "Super Admin":
            return True

        if not request.user.role:
            return False

        return request.user.role.permissions.filter(code=self.required_code).exists()


__all__ = ["IsAdmin", "IsSupportAgent", "HasPermissionCode"]
