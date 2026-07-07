from django.urls import path
from apps.reports.views import (
    OrdersReportView,
    RevenueReportView,
    CustomerReportView,
    ServicePopularityReportView,
    ZoneReportView,
)

app_name = "reports"

urlpatterns = [
    path("orders/", OrdersReportView.as_view(), name="orders_report"),
    path("revenue/", RevenueReportView.as_view(), name="revenue_report"),
    path("customers/", CustomerReportView.as_view(), name="customer_report"),
    path("services/", ServicePopularityReportView.as_view(), name="service_report"),
    path("zones/", ZoneReportView.as_view(), name="zone_report"),
]
