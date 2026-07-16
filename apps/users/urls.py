from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import (
    CustomerBlockView,
    UserViewSet,
)

app_name = "users"

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("<uuid:pk>/block/", CustomerBlockView.as_view(), name="customer_block"),
    path("", UserViewSet.as_view({"get": "list"}), name="customer_list"),
    path("<uuid:pk>/", UserViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name="customer_detail"),
    path("", include(router.urls)),
]
