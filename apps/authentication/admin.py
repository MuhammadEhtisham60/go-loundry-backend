from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.authentication.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the custom User model.
    Adapts Django's standard UserAdmin fields for the custom User attributes.
    """

    ordering = ("email",)
    list_display = (
        "email",
        "phone",
        "full_name",
        "role",
        "is_blocked",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_blocked", "is_staff", "is_active", "is_superuser")
    search_fields = ("email", "phone", "full_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "profile_photo",
                    "role",
                    "is_blocked",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone", "password", "full_name", "role"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("groups", "user_permissions")
