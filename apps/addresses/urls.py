from django.urls import path
from apps.addresses.views import AddressListView, AddressDetailView

app_name = "addresses"

urlpatterns = [
    path("", AddressListView.as_view(), name="address_list"),
    path("<uuid:pk>/", AddressDetailView.as_view(), name="address_detail"),
]
