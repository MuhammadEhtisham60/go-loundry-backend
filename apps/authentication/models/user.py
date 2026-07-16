import uuid
from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Customer"
    SUPPORT_AGENT = "SUPPORT_AGENT", "Support Agent"
    ADMIN = "ADMIN", "Admin"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"


class UserType(models.TextChoices):
    USER = "user", "User"
    ADMIN = "admin", "Admin"
    SUPER_ADMIN = "super_admin", "Super Admin"


class UserManager(BaseUserManager):
    """
    Custom user manager where email/phone is the unique identifier
    for authentication.
    """

    def create_user(
        self,
        email: str = None,
        phone: str = None,
        password: str = None,
        **extra_fields: Any
    ) -> "User":
        """
        Create and save a User with either email or phone and password.
        """
        if not email and not phone:
            raise ValueError("Either Email or Phone number must be set")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str = None, **extra_fields: Any
    ) -> "User":
        """
        Create and save a SuperUser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        from apps.authentication.models.role import Role
        role, _ = Role.objects.get_or_create(name="Super Admin")
        extra_fields.setdefault("role", role)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model supporting email/phone signup, profile metadata,
    role-based access control, OTP verification, and status flags.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, blank=True, db_index=True)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True, db_index=True)
    full_name = models.CharField(max_length=255, blank=True)
    profile_photo = models.URLField(max_length=500, null=True, blank=True)
    role = models.ForeignKey(
        "authentication.Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    avatar_initials = models.CharField(max_length=10, blank=True)
    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.USER
    )
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True, blank=True)
    invited_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invited_users"
    )
    invite_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("active", "Active")],
        default="active"
    )
    invite_token = models.CharField(max_length=255, null=True, blank=True, unique=True)

    # OTP for Phone registration/login and forgot password
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    # We keep email as the USERNAME_FIELD, but support alternative authentication backends
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.email or self.phone or str(self.id)

    def get_full_name(self) -> str:
        return self.full_name

    def get_short_name(self) -> str:
        return self.full_name.split(" ")[0] if self.full_name else ""

    @property
    def is_otp_expired(self) -> bool:
        """
        Check if the current OTP code has expired.
        """
        if not self.otp_expires_at:
            return True
        return timezone.now() > self.otp_expires_at

    def __init__(self, *args, **kwargs):
        role_val = kwargs.get("role")
        if isinstance(role_val, str):
            from apps.authentication.models.role import Role
            from django.utils.text import slugify
            role_name = role_val
            if role_name == "SUPER_ADMIN":
                role_name = "Super Admin"
            elif role_name == "ADMIN":
                role_name = "Admin"
            elif role_name == "SUPPORT_AGENT":
                role_name = "Support Agent"
            elif role_name == "CUSTOMER":
                role_name = "Customer"
            
            role_obj, _ = Role.objects.get_or_create(
                name=role_name,
                defaults={"slug": slugify(role_name)}
            )
            kwargs["role"] = role_obj
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if name == "role" and isinstance(value, str):
            from apps.authentication.models.role import Role
            from django.utils.text import slugify
            role_name = value
            if role_name == "SUPER_ADMIN":
                role_name = "Super Admin"
            elif role_name == "ADMIN":
                role_name = "Admin"
            elif role_name == "SUPPORT_AGENT":
                role_name = "Support Agent"
            elif role_name == "CUSTOMER":
                role_name = "Customer"
            
            role_obj, _ = Role.objects.get_or_create(
                name=role_name,
                defaults={"slug": slugify(role_name)}
            )
            value = role_obj
        super().__setattr__(name, value)

    def save(self, *args, **kwargs) -> None:
        if not self.avatar_initials and self.full_name:
            parts = self.full_name.strip().split()
            initials = "".join([p[0] for p in parts[:3] if p]).upper()
            self.avatar_initials = initials
        super().save(*args, **kwargs)
