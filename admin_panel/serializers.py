from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, EmailField, CharField

from accounts.models import User, RoleUserModel, RoleModel
from blog.models import BlogTagModel, AddBlogTagModel, BlogCategoryModel


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


class RoleSerializer(ModelSerializer):
    class Meta:
        model = RoleModel
        fields = '__all__'


class AddRoleSerializer(ModelSerializer):
    class Meta:
        model = RoleUserModel
        fields = '__all__'


class LoginUserSerializer(Serializer):
    email = EmailField()
    password = CharField(max_length=200)


class BlogTagSerializer(ModelSerializer):
    class Meta:
        model = BlogTagModel
        fields = '__all__'


class BlogCategorySerializer(ModelSerializer):
    class Meta:
        model = BlogCategoryModel
        fields = '__all__'


class AddBlogTagSerializer(ModelSerializer):
    class Meta:
        model = AddBlogTagModel
        fields = '__all__'
