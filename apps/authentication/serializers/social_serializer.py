from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    """
    Serializer validating inputs for Google/Facebook OAuth logins.
    """

    PLATFORM_CHOICES = (
        ("GOOGLE", "Google"),
        ("FACEBOOK", "Facebook"),
    )

    platform = serializers.ChoiceField(choices=PLATFORM_CHOICES, required=True)
    token = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=False, allow_blank=True, default="")
    profile_photo = serializers.URLField(required=False, allow_null=True, default=None)
