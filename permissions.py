from rest_framework.permissions import BasePermission
from accounts.models import RoleUserModel, RoleModel


class BlogPermission(BasePermission):
    def has_permission(self, request, view):
        return RoleUserModel.objects.filter(user=request.user, role=RoleModel.objects.get(role='blog')).exists()





