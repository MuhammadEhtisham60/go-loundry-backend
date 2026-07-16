from django.utils import timezone


class LastActiveMiddleware:
    """
    Middleware that updates the last_active timestamp on each authenticated request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            request.user.last_active = timezone.now()
            request.user.save(update_fields=["last_active"])

        return self.get_response(request)
