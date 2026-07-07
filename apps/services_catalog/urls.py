from django.urls import path
from apps.services_catalog.views import (
    ServiceListView,
    ServiceDetailView,
    ServiceReorderView,
)

app_name = "services_catalog"

urlpatterns = [
    path("", ServiceListView.as_view(), name="service_list"),
    path("<uuid:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("reorder/", ServiceReorderView.as_view(), name="service_reorder"),
]
