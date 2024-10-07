from rest_framework.permissions import BasePermission
from accounts.models import RoleUserModel, RoleModel


class IsBlogAdmin(BasePermission):
    def has_permission(self, request, view):

        return (RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='blog')).exists() or
                request.user.is_superuser)


class IsProductAdmin(BasePermission):
    def has_permission(self, request, view):
        return (RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='product')).exists() or
                request.user.is_superuser)


class IsOrderAdmin(BasePermission):
    def has_permission(self, request, view):
        return (RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='order')).exists() or
                request.user.is_superuser)


class IsSEOAdmin(BasePermission):
    def has_permission(self, request, view):
        return (RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='seo')).exists() or
                request.user.is_superuser)


class IsModeratorAdmin(BasePermission):
    def has_permission(self, request, view):
        return (RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='moderator')).exists()
                or request.user.is_superuser)


class IsAccountAdmin(BasePermission):
    def has_permission(self, request, view):
        return (RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='account')).exists()
                or request.user.is_superuser)


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class OrPermission(BasePermission):
    def __init__(self, *perms):
        self.perms = perms

    def has_permission(self, request, view):
        return any(perm().has_permission(request, view) for perm in self.perms)

    def has_object_permission(self, request, view, obj):
        return any(perm().has_object_permission(request, view, obj) for perm in self.perms)
