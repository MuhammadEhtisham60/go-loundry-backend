import secrets
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from apps.authentication.models.role import Role, Permission
from apps.users.permissions import HasPermissionCode
from apps.users.serializers.team_serializers import (
    RoleSerializer,
    RoleWriteSerializer,
    PermissionSerializer,
    UserListSerializer,
    UserWriteSerializer,
    UserInviteSerializer,
    CompleteSignupSerializer,
)
from apps.authentication.services.auth_service import AuthService
from apps.authentication.serializers.user_serializer import UserSerializer as AuthUserSerializer
from common.responses.standard import StandardResponse

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing back-office team members, inviting them, and completing sign-ups.
    """

    queryset = User.objects.filter(role__isnull=False)

    def get_permissions(self):
        if self.action == "complete_signup":
            return [AllowAny()]
        
        # If listing or retrieving customers (no team param), default to IsSupportAgent
        if self.action in ["list", "retrieve"]:
            role_param = self.request.query_params.get("role")
            type_param = self.request.query_params.get("type")
            if role_param != "team" and type_param != "team":
                from apps.users.permissions import IsSupportAgent
                return [IsAuthenticated(), IsSupportAgent()]

        return [IsAuthenticated(), HasPermissionCode("users")]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserWriteSerializer
        return UserListSerializer

    def list(self, request, *args, **kwargs) -> Response:
        role_param = request.query_params.get("role")
        type_param = request.query_params.get("type")
        if role_param == "team" or type_param == "team":
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return StandardResponse(
                data=serializer.data,
                message="Team members retrieved successfully.",
                status=status.HTTP_200_OK,
            )

        # Fallback to customer list (keeps backward compatibility!)
        search = request.query_params.get("search")
        is_blocked_str = request.query_params.get("is_blocked")
        is_blocked = None
        if is_blocked_str is not None:
            is_blocked = is_blocked_str.lower() == "true"

        from apps.users.selectors import UserSelector
        from apps.users.serializers import CustomerListSerializer
        customers = UserSelector.get_customers(search_query=search, is_blocked=is_blocked)
        serializer = CustomerListSerializer(customers, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Customer records list retrieved.",
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None, *args, **kwargs) -> Response:
        user = get_object_or_404(User, pk=pk)
        if user.role and user.role.name in ["Super Admin", "Admin", "Support Agent"]:
            serializer = UserListSerializer(user)
            return StandardResponse(
                data=serializer.data,
                message="User retrieved successfully.",
                status=status.HTTP_200_OK,
            )
        else:
            from apps.users.serializers import CustomerDetailSerializer
            serializer = CustomerDetailSerializer(user)
            return StandardResponse(
                data=serializer.data,
                message="Customer details retrieved.",
                status=status.HTTP_200_OK,
            )

    def update(self, request, pk=None, *args, **kwargs) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user, data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)

        # Validation: check if deactivating the last active Super Admin
        is_active = request.data.get("is_active")
        if is_active is False and user.role and user.role.name == "Super Admin":
            super_admins_count = User.objects.filter(role__name="Super Admin", is_active=True).count()
            if super_admins_count <= 1:
                return Response(
                    {"message": "Cannot deactivate the last remaining Super Admin."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        updated_user = serializer.save()
        return StandardResponse(
            data=UserListSerializer(updated_user).data,
            message="User updated successfully.",
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None, *args, **kwargs) -> Response:
        user = get_object_or_404(User, pk=pk)

        # Validation: check if deleting the last active Super Admin
        if user.role and user.role.name == "Super Admin":
            super_admins_count = User.objects.filter(role__name="Super Admin", is_active=True).count()
            if super_admins_count <= 1:
                return Response(
                    {"message": "Cannot delete the last remaining Super Admin."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user.delete()
        return StandardResponse(
            data=None,
            message="User deleted successfully.",
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, HasPermissionCode("users")], url_path="invite")
    def invite(self, request) -> Response:
        """
        Invites a new team member and returns a secure token link (stub).
        """
        serializer = UserInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data["full_name"]
        email = serializer.validated_data["email"]
        role_id = serializer.validated_data["role_id"]

        role = get_object_or_404(Role, id=role_id)
        token = secrets.token_urlsafe(32)

        # Create user as pending
        user = User.objects.create(
            email=email,
            full_name=full_name,
            role=role,
            is_active=False,
            invite_status="pending",
            invite_token=token,
            invited_by=request.user,
        )

        invite_link = f"http://localhost:5173/complete-signup?token={token}"
        print(f"DEBUG: Sent invite email to {email} with link: {invite_link}")

        return StandardResponse(
            data={
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "invite_token": token,
                "invite_link": invite_link,
            },
            message="User invited successfully.",
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny], url_path="complete-signup")
    def complete_signup(self, request) -> Response:
        """
        Completes registration for an invited user.
        """
        serializer = CompleteSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(invite_token=token, invite_status="pending").first()
        if not user:
            return Response(
                {"message": "Invalid or expired invite token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Activate user account
        user.set_password(password)
        user.is_active = True
        user.invite_status = "active"
        user.invite_token = None
        user.last_active = timezone.now()
        user.save()

        # Generate tokens
        tokens = AuthService.generate_tokens(user)

        return StandardResponse(
            data={
                "tokens": tokens,
                "user": AuthUserSerializer(user).data,
            },
            message="Signup completed successfully.",
            status=status.HTTP_200_OK,
        )


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Roles and permission association.
    """

    queryset = Role.objects.all()
    permission_classes = [IsAuthenticated, HasPermissionCode("users")]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RoleWriteSerializer
        return RoleSerializer

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Roles list retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None, *args, **kwargs) -> Response:
        role = get_object_or_404(Role, pk=pk)
        serializer = self.get_serializer(role)
        return StandardResponse(
            data=serializer.data,
            message="Role retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        return StandardResponse(
            data=RoleSerializer(role).data,
            message="Role created successfully.",
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None, *args, **kwargs) -> Response:
        role = get_object_or_404(Role, pk=pk)
        serializer = self.get_serializer(role, data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        updated_role = serializer.save()
        return StandardResponse(
            data=RoleSerializer(updated_role).data,
            message="Role updated successfully.",
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None, *args, **kwargs) -> Response:
        role = get_object_or_404(Role, pk=pk)

        # Block deletion if users are assigned to this role
        if role.users.exists():
            return Response(
                {"message": "Cannot delete role because users are assigned to it."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        role.delete()
        return StandardResponse(
            data=None,
            message="Role deleted successfully.",
            status=status.HTTP_200_OK,
        )


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing available permission codes and labels.
    """

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, HasPermissionCode("users")]

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Permissions list retrieved successfully.",
            status=status.HTTP_200_OK,
        )
