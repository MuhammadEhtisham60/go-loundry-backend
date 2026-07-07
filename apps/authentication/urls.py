from django.urls import path
from apps.authentication.views import (
    RegisterView,
    LoginView,
    ProfileView,
    CustomTokenRefreshView,
    OtpTriggerView,
    OtpVerifyView,
    ForgotPasswordView,
    ResetPasswordView,
    SocialLoginView,
)

app_name = "authentication"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/otp/", OtpTriggerView.as_view(), name="otp_trigger"),
    path("login/otp/verify/", OtpVerifyView.as_view(), name="otp_verify"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("social-login/", SocialLoginView.as_view(), name="social_login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
