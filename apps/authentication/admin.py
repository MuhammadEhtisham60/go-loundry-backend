from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.authentication.models import User, Role, Permission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    filter_horizontal = ("permissions",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")


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
        "invite_status",
    )
    list_filter = ("role", "is_blocked", "is_staff", "is_active", "is_superuser", "invite_status")
    search_fields = ("email", "phone", "full_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "full_name",
                    "avatar_initials",
                    "phone",
                    "profile_photo",
                    "role",
                    "is_blocked",
                )
            },
        ),
        (
            "Invite Tracking",
            {
                "fields": (
                    "invited_by",
                    "invite_status",
                    "invite_token",
                    "last_active",
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
                "fields": ("email", "phone", "password", "full_name", "role", "avatar_initials"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "last_active")
    filter_horizontal = ("groups", "user_permissions")
