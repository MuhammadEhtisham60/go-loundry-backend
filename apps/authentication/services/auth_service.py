import random
from datetime import timedelta
from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.services.notifications import NotificationService

User = get_user_model()


class AuthService:
    """
    Service layer containing all core authentication workflows (registrations, logins,
    OTP code triggers & verifications, social integrations, and password resets).
    """

    @staticmethod
    def register_user(validated_data: Dict[str, Any]) -> User:
        """
        Register a new user (via email, phone, or both) with optional password.
        """
        email = validated_data.get("email")
        phone = validated_data.get("phone")
        password = validated_data.get("password")
        full_name = validated_data.get("full_name", "")
        user_type = validated_data.get("user_type", "user")

        user = User.objects.create_user(
            email=email,
            phone=phone,
            password=password,
            full_name=full_name,
            user_type=user_type,
        )
        return user

    @staticmethod
    def generate_tokens(user: User) -> Dict[str, str]:
        """
        Generate access and refresh tokens for a user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def trigger_otp(
        email: Optional[str] = None, phone: Optional[str] = None
    ) -> User:
        """
        Generate a 6-digit OTP code, save it on the user object, and simulate sending it.
        Creates a user if a phone registration is requested and doesn't exist.
        """
        if not email and not phone:
            raise serializers.ValidationError("Email or phone is required to trigger OTP.")

        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("User with this email does not exist.")
        else:
            # Auto-create user if they log in via phone and don't exist yet
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={"full_name": "Phone User"},
            )

        # Generate 6-digit code
        otp = f"{random.randint(100000, 999999)}"
        user.otp_code = otp
        user.otp_expires_at = timezone.now() + timedelta(minutes=5)
        user.save()

        # Send OTP
        message = f"Your GoLaundry verification code is {otp}. Valid for 5 minutes."
        if user.phone:
            NotificationService.send_sms(user.phone, message)
        if user.email:
            NotificationService.send_email(
                user.id, user.email, "Verification Code", message
            )

        return user

    @staticmethod
    def verify_otp(
        otp_code: str, email: Optional[str] = None, phone: Optional[str] = None
    ) -> User:
        """
        Verify the provided OTP code. If valid, clears the OTP and returns the User.
        """
        if email:
            user = User.objects.filter(email=email).first()
        else:
            user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError("User account not found.")

        if user.is_blocked:
            raise serializers.ValidationError("This user account is blocked.")

        if user.otp_code != otp_code or user.is_otp_expired:
            raise serializers.ValidationError("Invalid or expired verification code.")

        # Clear OTP upon successful verification
        user.otp_code = None
        user.otp_expires_at = None
        user.save()

        return user

    @staticmethod
    def forgot_password(
        email: Optional[str] = None, phone: Optional[str] = None
    ) -> User:
        """
        Initiates the forgot-password flow by triggering an OTP.
        """
        return AuthService.trigger_otp(email=email, phone=phone)

    @staticmethod
    def reset_password(
        validated_data: Dict[str, Any]
    ) -> User:
        """
        Completes the password reset process by verifying the OTP and saving the new password.
        """
        email = validated_data.get("email")
        phone = validated_data.get("phone")
        otp_code = validated_data.get("otp_code")
        new_password = validated_data.get("new_password")

        user = AuthService.verify_otp(otp_code=otp_code, email=email, phone=phone)
        user.set_password(new_password)
        user.save()
        return user

    @staticmethod
    def social_login(validated_data: Dict[str, Any]) -> User:
        """
        Handles the social authentication callback.
        Finds or creates the user and signs them in.
        """
        email = validated_data["email"]
        full_name = validated_data.get("full_name", "")
        profile_photo = validated_data.get("profile_photo", "")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "profile_photo": profile_photo,
            },
        )

        if user.is_blocked:
            raise serializers.ValidationError("Your account has been blocked.")

        return user
