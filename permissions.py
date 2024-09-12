from rest_framework.permissions import BasePermission
from accounts.models import RoleUserModel, RoleModel


class IsBlogAdmin(BasePermission):
    def has_permission(self, request, view):
        # if request.method in ['POST', 'PUT', 'PATCH']:
        #     return RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='blog')).exists()
        # return True
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
