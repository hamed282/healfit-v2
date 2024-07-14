from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField
from accounts.models import User, RoleUserModel
from django.shortcuts import get_object_or_404


class UserSerializer(ModelSerializer):
    role = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role']

    def get_role(self, obj):
        try:
            role = RoleUserModel.objects.get(user=obj)
            role = role.role.role
        except:
            role = 'user'

        return role


class UserValueSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login')

