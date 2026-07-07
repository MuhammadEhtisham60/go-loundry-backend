from apps.authentication.views.register_view import RegisterView
from apps.authentication.views.login_view import LoginView
from apps.authentication.views.profile_view import ProfileView
from apps.authentication.views.token_refresh_view import CustomTokenRefreshView
from apps.authentication.views.otp_view import OtpTriggerView, OtpVerifyView
from apps.authentication.views.password_reset_view import (
    ForgotPasswordView,
    ResetPasswordView,
)
from apps.authentication.views.social_view import SocialLoginView

__all__ = [
    "RegisterView",
    "LoginView",
    "ProfileView",
    "CustomTokenRefreshView",
    "OtpTriggerView",
    "OtpVerifyView",
    "ForgotPasswordView",
    "ResetPasswordView",
    "SocialLoginView",
]
