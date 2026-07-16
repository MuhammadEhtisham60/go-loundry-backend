from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.locations.models import WarehouseSetting
from apps.locations.services import LocationService
from apps.locations.selectors import LocationSelector
from apps.locations.serializers import (
    WarehouseSettingSerializer,
    DeliveryTierSerializer,
    ValidateAreaSerializer,
)
from apps.locations.permissions import IsSuperAdmin
from common.responses.standard import StandardResponse


class WarehouseSettingView(APIView):
    """
    API View to list and create warehouse configurations.
    GET is public; POST requires Super Admin.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsSuperAdmin()]

    def get(self, request: Request) -> Response:
        warehouses = WarehouseSetting.objects.all().order_by("-created_at")
        serializer = WarehouseSettingSerializer(warehouses, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Warehouse settings retrieved.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = WarehouseSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        warehouse = serializer.save()
        return StandardResponse(
            data=WarehouseSettingSerializer(warehouse).data,
            message="Warehouse settings created successfully.",
            status=status.HTTP_201_CREATED,
        )


class WarehouseDetailView(APIView):
    """
    API View to retrieve, update, and delete a specific warehouse configuration.
    GET is public; PUT and DELETE require Super Admin.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsSuperAdmin()]

    def get(self, request: Request, pk: int) -> Response:
        try:
            warehouse = WarehouseSetting.objects.get(pk=pk)
            serializer = WarehouseSettingSerializer(warehouse)
            return StandardResponse(
                data=serializer.data,
                message="Warehouse settings retrieved.",
                status=status.HTTP_200_OK,
            )
        except WarehouseSetting.DoesNotExist:
            return StandardResponse(
                data=None,
                message="Warehouse not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )

    def put(self, request: Request, pk: int) -> Response:
        try:
            warehouse = WarehouseSetting.objects.get(pk=pk)
            serializer = WarehouseSettingSerializer(warehouse, data=request.data)
            serializer.is_valid(raise_exception=True)
            warehouse = serializer.save()
            return StandardResponse(
                data=WarehouseSettingSerializer(warehouse).data,
                message="Warehouse settings updated successfully.",
                status=status.HTTP_200_OK,
            )
        except WarehouseSetting.DoesNotExist:
            return StandardResponse(
                data=None,
                message="Warehouse not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )

    def delete(self, request: Request, pk: int) -> Response:
        try:
            warehouse = WarehouseSetting.objects.get(pk=pk)
            warehouse.delete()
            return StandardResponse(
                data=None,
                message="Warehouse settings deleted successfully.",
                status=status.HTTP_200_OK,
            )
        except WarehouseSetting.DoesNotExist:
            return StandardResponse(
                data=None,
                message="Warehouse not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )


class DeliveryTierView(APIView):
    """
    API View to list and create/replace delivery tiers.
    GET is public; POST and PUT require Super Admin.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsSuperAdmin()]

    def get(self, request: Request) -> Response:
        tiers = LocationSelector.list_delivery_tiers()
        serializer = DeliveryTierSerializer(tiers, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Delivery tiers list retrieved.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = DeliveryTierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tier = serializer.save()
        return StandardResponse(
            data=DeliveryTierSerializer(tier).data,
            message="Delivery tier created successfully.",
            status=status.HTTP_201_CREATED,
        )

    def put(self, request: Request) -> Response:
        serializer = DeliveryTierSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        tiers = LocationService.bulk_update_tiers(serializer.validated_data)
        return StandardResponse(
            data=DeliveryTierSerializer(tiers, many=True).data,
            message="Delivery tiers saved successfully.",
            status=status.HTTP_200_OK,
        )


class DeliveryTierDetailView(APIView):
    """
    API View to manage specific delivery tiers.
    Requires Super Admin privileges.
    """

    permission_classes = [IsSuperAdmin]

    def delete(self, request: Request, pk: int) -> Response:
        from apps.locations.models import DeliveryTier

        try:
            tier = DeliveryTier.objects.get(pk=pk)
            tier.delete()
            return StandardResponse(
                data=None,
                message="Delivery tier deleted successfully.",
                status=status.HTTP_200_OK,
            )
        except DeliveryTier.DoesNotExist:
            return StandardResponse(
                data=None,
                message="Delivery tier not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )


class ValidateAreaView(APIView):
    """
    API View to check if coordinates are within warehouse service bounds
    and calculate estimated shipping costs.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = ValidateAreaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = LocationService.validate_service_area(
            latitude=serializer.validated_data["latitude"],
            longitude=serializer.validated_data["longitude"],
        )

        return StandardResponse(
            data=result,
            message="Location checked successfully.",
            status=status.HTTP_200_OK,
        )
