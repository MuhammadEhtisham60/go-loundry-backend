from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.addresses.services import AddressService
from apps.addresses.selectors import AddressSelector
from apps.addresses.serializers import AddressSerializer
from apps.addresses.permissions import IsCustomer
from common.responses.standard import StandardResponse


class AddressListView(APIView):
    """
    API View to list and create customer addresses.
    Requires user to be authenticated and have CUSTOMER role.
    """

    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request: Request) -> Response:
        addresses = AddressSelector.get_user_addresses(request.user)
        serializer = AddressSerializer(addresses, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Addresses list retrieved.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = AddressService.create_address(
            user=request.user, validated_data=serializer.validated_data
        )
        result_serializer = AddressSerializer(address)

        return StandardResponse(
            data=result_serializer.data,
            message="Address created successfully.",
            status=status.HTTP_201_CREATED,
        )


class AddressDetailView(APIView):
    """
    API View to retrieve, update, and delete individual saved customer addresses.
    Requires user to be authenticated and have CUSTOMER role.
    """

    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request: Request, pk: str) -> Response:
        address = AddressSelector.get_address_by_id(request.user, pk)
        if not address:
            return StandardResponse(
                data=None,
                message="Address not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )

        serializer = AddressSerializer(address)
        return StandardResponse(
            data=serializer.data,
            message="Address details retrieved.",
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, pk: str) -> Response:
        serializer = AddressSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        address = AddressService.update_address(
            user=request.user, address_id=pk, validated_data=serializer.validated_data
        )
        result_serializer = AddressSerializer(address)

        return StandardResponse(
            data=result_serializer.data,
            message="Address updated successfully.",
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, pk: str) -> Response:
        AddressService.delete_address(user=request.user, address_id=pk)
        return StandardResponse(
            data=None,
            message="Address deleted successfully.",
            status=status.HTTP_200_OK,
        )
