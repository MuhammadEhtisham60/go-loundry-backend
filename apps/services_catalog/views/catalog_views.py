from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.services_catalog.models import Service
from apps.services_catalog.services import CatalogService
from apps.services_catalog.selectors import CatalogSelector
from apps.services_catalog.serializers import (
    ServiceSerializer,
    ReorderServiceListSerializer,
)
from apps.services_catalog.permissions import IsAdmin
from common.responses.standard import StandardResponse


class ServiceListView(APIView):
    """
    API View to list and create services.
    GET is accessible to everyone (filter active services only for customers, returns all for Admin).
    POST requires Admin permissions.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdmin()]

    def get(self, request: Request) -> Response:
        # Determine if caller has administrative privileges to view inactive catalog items
        is_admin_user = (
            request.user
            and request.user.is_authenticated
            and (
                request.user.role in ["ADMIN", "SUPER_ADMIN"]
                or request.user.user_type in ["admin", "super_admin"]
            )
        )

        include_inactive = is_admin_user and request.query_params.get(
            "include_inactive", "true"
        ).lower() == "true"

        services = CatalogSelector.get_all_services(
            include_inactive=include_inactive
        )
        serializer = ServiceSerializer(services, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Services catalog retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = ServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CatalogService.create_service(serializer.validated_data)
        result_serializer = ServiceSerializer(service)

        return StandardResponse(
            data=result_serializer.data,
            message="Catalog service created successfully.",
            status=status.HTTP_201_CREATED,
        )


class ServiceDetailView(APIView):
    """
    API View to retrieve, update, and soft-delete individual service items.
    GET is public; PUT, PATCH, and DELETE require Admin privileges.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdmin()]

    def get(self, request: Request, pk: str) -> Response:
        is_admin_user = (
            request.user
            and request.user.is_authenticated
            and (
                request.user.role in ["ADMIN", "SUPER_ADMIN"]
                or request.user.user_type in ["admin", "super_admin"]
            )
        )

        service = get_object_or_404(Service, id=pk)

        if not is_admin_user and not service.is_active:
            from django.http import Http404
            raise Http404("No Service matches the given query.")

        serializer = ServiceSerializer(service)
        return StandardResponse(
            data=serializer.data,
            message="Service details retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, pk: str) -> Response:
        serializer = ServiceSerializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        service = CatalogService.update_service(pk, serializer.validated_data)
        result_serializer = ServiceSerializer(service)

        return StandardResponse(
            data=result_serializer.data,
            message="Catalog service updated successfully.",
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, pk: str) -> Response:
        serializer = ServiceSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = CatalogService.update_service(pk, serializer.validated_data)
        result_serializer = ServiceSerializer(service)

        return StandardResponse(
            data=result_serializer.data,
            message="Catalog service updated successfully.",
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, pk: str) -> Response:
        CatalogService.soft_delete_service(pk)
        return StandardResponse(
            data=None,
            message="Catalog service deleted successfully.",
            status=status.HTTP_200_OK,
        )


class ServiceReorderView(APIView):
    """
    API View to update sequence numbers in bulk.
    Requires Admin privileges.
    """

    permission_classes = [IsAdmin]

    def post(self, request: Request) -> Response:
        serializer = ReorderServiceListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CatalogService.reorder_services(serializer.validated_data["services"])

        return StandardResponse(
            data=None,
            message="Catalog service display ordering updated.",
            status=status.HTTP_200_OK,
        )
