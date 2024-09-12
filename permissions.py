from rest_framework.permissions import BasePermission
from accounts.models import RoleUserModel, RoleModel


class IsBlogAdmin(BasePermission):
    def has_permission(self, request, view):
        # if request.method in ['POST', 'PUT', 'PATCH']:
        #     return RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='blog')).exists()
        # return True
        return RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='blog')).exists()


class IsProductAdmin(BasePermission):
    def has_permission(self, request, view):
        return RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='product')).exists()


class IsOrderAdmin(BasePermission):
    def has_permission(self, request, view):
        return RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='order')).exists()
