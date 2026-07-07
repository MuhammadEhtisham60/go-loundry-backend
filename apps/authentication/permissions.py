from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import models
from apps.authentication.models.user import UserRole


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access/edit it.
    Assumes the model instance has a 'user' attribute.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: models.Model) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "user", None) == request.user


class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to Super Admins.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.SUPER_ADMIN
        )


class IsAdmin(permissions.BasePermission):
    """
    Allows access to Admins and Super Admins.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
        )


class IsSupportAgent(permissions.BasePermission):
    """
    Allows access to Support Agents, Admins, and Super Admins.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            in [UserRole.SUPPORT_AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]
        )


class IsCustomer(permissions.BasePermission):
    """
    Allows access only to Customers.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.CUSTOMER
        )
