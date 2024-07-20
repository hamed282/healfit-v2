from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, EmailField, CharField
from rest_framework import serializers
from accounts.models import User, RoleUserModel, RoleModel
from blog.models import BlogTagModel, AddBlogTagModel, BlogCategoryModel, BlogModel
from django.utils.text import slugify
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


class BlogModelSerializer(ModelSerializer):
    class Meta:
        model = BlogModel
        fields = '__all__'


class AddBlogTagSerializer(ModelSerializer):
    class Meta:
        model = AddBlogTagModel
        fields = '__all__'


class CombinedBlogSerializer(serializers.Serializer):
    cover_image = serializers.ImageField()
    cover_image_alt = serializers.CharField(max_length=32)
    banner = serializers.ImageField()
    banner_alt = serializers.CharField(max_length=32)
    title = serializers.CharField(max_length=250)
    title_image = serializers.ImageField()
    title_image_alt = serializers.CharField(max_length=32)
    short_description = serializers.CharField(max_length=60)
    description = serializers.CharField()
    body = serializers.CharField()
    author = serializers.CharField(max_length=64)
    role = serializers.CharField(max_length=24)
    slug = serializers.SlugField()
    # category = serializers.PrimaryKeyRelatedField(queryset=BlogCategoryModel.objects.all())
    category = serializers.CharField(max_length=100)
    follow = serializers.BooleanField(default=False)
    index = serializers.BooleanField(default=False)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60)
    meta_description = serializers.CharField(max_length=150)
    tag = serializers.PrimaryKeyRelatedField(queryset=BlogTagModel.objects.all(), required=False, allow_null=True)

    def create(self, validated_data):
        # Extract tag data
        tag = validated_data.pop('tag', None)

        category_name = validated_data.pop('category')
        category = get_object_or_404(BlogCategoryModel, category=category_name)
        validated_data['category'] = category

        # Generate unique slug
        original_slug = slugify(validated_data['slug'])
        unique_slug = original_slug
        num = 1
        while BlogModel.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{original_slug}-{num}'
            num += 1
        validated_data['slug'] = unique_slug

        # Create BlogModel instance
        blog = BlogModel.objects.create(**validated_data)

        # Create AddBlogTagModel instance if tag is provided
        if tag:
            AddBlogTagModel.objects.create(blog=blog, tag=tag)

        return blog

    def update(self, instance, validated_data):
        # به روز رسانی مدل
        tag = validated_data.pop('tag', None)
        category_name = validated_data.pop('category', None)
        if category_name:
            category, created = BlogCategoryModel.objects.get_or_create(name=category_name)
            validated_data['category'] = category
        else:
            validated_data['category'] = instance.category

        # به روز رسانی فیلدهای BlogModel
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # به روز رسانی AddBlogTagModel اگر موجود باشد
        if tag:
            AddBlogTagModel.objects.update_or_create(blog=instance, defaults={'tag': tag})
        elif hasattr(instance, 'blog_tag'):
            instance.blog_tag.delete()

        return instance

    def to_representation(self, instance):
        blog_data = BlogModelSerializer(instance).data
        category_data = BlogCategorySerializer(instance.category).data
        tag_data = AddBlogTagSerializer(instance.blog_tag).data if hasattr(instance, 'blog_tag') else None
        return {**blog_data, 'category': category_data['category'], 'tag': tag_data['id'] if tag_data else None}