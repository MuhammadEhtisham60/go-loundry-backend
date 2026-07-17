from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.authentication.models.role import Role, Permission

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer representing granular system permissions.
    """

    class Meta:
        model = Permission
        fields = ("id", "code", "label")


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer representing roles with nested permissions list.
    """

    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ("id", "name", "slug", "permissions", "created_at", "updated_at")


class RoleWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating roles by name and permission codes.
    """

    permission_codes = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Role
        fields = ("id", "name", "permission_codes")

    def validate_name(self, value: str) -> str:
        qs = Role.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Role with this name already exists.")
        return value

    def create(self, validated_data: dict) -> Role:
        permission_codes = validated_data.pop("permission_codes", [])
        role = Role.objects.create(**validated_data)
        permissions = Permission.objects.filter(code__in=permission_codes)
        role.permissions.set(permissions)
        return role

    def update(self, instance: Role, validated_data: dict) -> Role:
        permission_codes = validated_data.pop("permission_codes", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if permission_codes is not None:
            permissions = Permission.objects.filter(code__in=permission_codes)
            instance.permissions.set(permissions)
        return instance


class UserRoleNestedSerializer(serializers.ModelSerializer):
    """
    Serializer representing nested role values for user list.
    """

    class Meta:
        model = Role
        fields = ("id", "name")


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer representing active team members list.
    """

    role = UserRoleNestedSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "avatar_initials",
            "role",
            "last_active",
            "invite_status",
            "is_active",
        )


class UserWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing user fields.
    """

    role_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("full_name", "email", "role_id", "is_active")

    def validate_email(self, value: str) -> str:
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def update(self, instance: User, validated_data: dict) -> User:
        role_id = validated_data.pop("role_id", None)
        if role_id is not None:
            try:
                role = Role.objects.get(id=role_id)
                instance.role = role
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role_id": "Role does not exist."})
        elif "role_id" in validated_data:
            instance.role = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserInviteSerializer(serializers.Serializer):
    """
    Validation payload for creating a new team member with auto-generated credentials.
    """

    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    role_id = serializers.IntegerField()
    user_type = serializers.ChoiceField(
        choices=["user", "admin", "super_admin"],
        default="admin",
        required=False,
    )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value: str) -> str:
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def validate_role_id(self, value: int) -> int:
        if not Role.objects.filter(id=value).exists():
            raise serializers.ValidationError("Role does not exist.")
        return value



class CompleteSignupSerializer(serializers.Serializer):
    """
    Validation payload for finalizing registration.
    """

    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)


class LoginSerializer(serializers.Serializer):
    """
    Validation payload for team authentication.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
