from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # App API routes
    path("api/auth/", include("apps.authentication.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/addresses/", include("apps.addresses.urls")),
    path("api/locations/", include("apps.locations.urls")),
    path("api/services/", include("apps.services_catalog.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/reviews/", include("apps.reviews.urls")),
    path("api/chats/", include("apps.chats.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/admin/dashboard/", include("apps.dashboard.urls")),
    path("api/admin/reports/", include("apps.reports.urls")),
]
