from django.urls import path
from apps.users.views import (
    CustomerListView,
    CustomerDetailView,
    CustomerBlockView,
)

app_name = "users"

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer_list"),
    path("<uuid:pk>/", CustomerDetailView.as_view(), name="customer_detail"),
    path("<uuid:pk>/block/", CustomerBlockView.as_view(), name="customer_block"),
]
