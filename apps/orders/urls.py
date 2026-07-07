from django.urls import path
from apps.orders.views import (
    OrderListView,
    OrderDetailView,
    OrderCancelView,
    OrderStatusUpdateView,
    OrderReorderView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("<uuid:pk>/cancel/", OrderCancelView.as_view(), name="order_cancel"),
    path("<uuid:pk>/status/", OrderStatusUpdateView.as_view(), name="order_status_update"),
    path("<uuid:pk>/reorder/", OrderReorderView.as_view(), name="order_reorder"),
]
