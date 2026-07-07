from django.urls import path
from apps.locations.views import (
    WarehouseSettingView,
    DeliveryTierView,
    DeliveryTierDetailView,
    ValidateAreaView,
)

app_name = "locations"

urlpatterns = [
    path("warehouse/", WarehouseSettingView.as_view(), name="warehouse_setting"),
    path("tiers/", DeliveryTierView.as_view(), name="tiers"),
    path("tiers/<int:pk>/", DeliveryTierDetailView.as_view(), name="tier_detail"),
    path("validate-area/", ValidateAreaView.as_view(), name="validate_area"),
]
