from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, EmailField, CharField
from rest_framework import serializers
from accounts.models import User, RoleUserModel, RoleModel
from blog.models import BlogTagModel, AddBlogTagModel, BlogCategoryModel, BlogModel
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from product.models import (ExtraGroupModel, SizeProductModel, ColorProductModel, AddImageGalleryModel, ProductTagModel,
                            ProductSubCategoryModel, ProductModel, AddProductTagModel, ProductGenderModel,
                            AddSubCategoryModel)
from product.serializers import ProductSerializer, ProductColorImageSerializer


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
            category, created = BlogCategoryModel.objects.get_or_create(category=category_name)
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
        return {**blog_data, 'category': category_data['category'], 'tag': tag_data['tag'] if tag_data else None}


class ExtraGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraGroupModel
        fields = '__all__'


class ColorValueSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = ColorProductModel
        fields = ['id', 'value', 'type', 'title']

    def get_value(self, obj):
        value = obj.color_code
        return value

    def get_type(self, obj):
        return 'color'

    def get_title(self, obj):
        title = obj.color
        return title


class ColorValueCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorProductModel
        fields = '__all__'


class SizeValueSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()

    class Meta:
        model = SizeProductModel
        fields = ['id', 'value', 'type', 'priority']

    def get_value(self, obj):
        value = obj.size
        return value

    def get_type(self, obj):
        return 'text'

    def get_priority(self, obj):
        priority = obj.priority
        return priority


class SizeValueCUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = SizeProductModel
        fields = '__all__'


class AddImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddImageGalleryModel
        fields = '__all__'


class ProductTagSerializer(ModelSerializer):
    class Meta:
        model = ProductTagModel
        fields = '__all__'


class CombinedProductSerializer(serializers.Serializer):
    gender = serializers.PrimaryKeyRelatedField(queryset=ProductGenderModel.objects.all())
    product = serializers.CharField()
    description_image = serializers.ImageField()
    description_image_alt = serializers.CharField()
    size_table_image = serializers.ImageField()
    size_table_image_alt = serializers.CharField()
    cover_image = serializers.ImageField()
    cover_image_alt = serializers.CharField()
    price = serializers.CharField()
    percent_discount = serializers.IntegerField()
    subtitle = serializers.CharField()
    application_fields = serializers.CharField()
    description = serializers.CharField()
    group_id = serializers.CharField()
    priority = serializers.IntegerField()
    slug = serializers.SlugField()

    subcategory = serializers.CharField(max_length=100)
    follow = serializers.BooleanField(default=False)
    index = serializers.BooleanField(default=False)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60)
    meta_description = serializers.CharField(max_length=150)
    tag_name = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def create(self, validated_data):
        # Extract and process tag data
        tag_name = validated_data.pop('tag_name', None)
        tag = None
        if tag_name:
            tag, created = ProductTagModel.objects.get_or_create(tag=tag_name)

        # Generate unique slug
        original_slug = slugify(validated_data['slug'])
        unique_slug = original_slug

        num = 1
        while ProductModel.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{original_slug}-{num}'
            num += 1
        validated_data['slug'] = unique_slug

        subcategory_name = validated_data.pop('subcategory', [])
        subcategory_name = subcategory_name
        # Create ProductModel instance
        product = ProductModel.objects.create(**validated_data)

        subcategory_name = subcategory_name.split(',')
        for sub in subcategory_name:
            subcategory = get_object_or_404(ProductSubCategoryModel, subcategory=sub)
            # Create AddSubCategoryModel instance
            AddSubCategoryModel.objects.create(product=product, subcategory=subcategory)

        # Create AddProductTagModel instance if tag is provided
        try:
            if tag:
                AddProductTagModel.objects.create(product=product, tag=tag)
        except:
            # raise ValueError('Email must be')
            pass

        return product

    def update(self, instance, validated_data):
        # Update the ProductModel instance
        tag_name = validated_data.pop('tag_name', None)
        subcategory_name = validated_data.pop('subcategory', None)

        if subcategory_name:
            subcategory = get_object_or_404(ProductSubCategoryModel, subcategory=subcategory_name)
            instance.subcategory = subcategory

        if tag_name:
            tag, created = ProductTagModel.objects.get_or_create(tag=tag_name)
        else:
            tag = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update or delete AddProductTagModel instance
        if tag:
            AddProductTagModel.objects.update_or_create(product=instance, defaults={'tag': tag})
        elif hasattr(instance, 'product_tag'):
            instance.product_tag.delete()

        return instance

    def to_representation(self, instance):
        product_data = ProductSerializer(instance).data
        print(instance)
        # subcategory_data = instance.subcategory.subcategory if instance.subcategory else None
        tag_data = instance.product_tag.tag.tag if hasattr(instance, 'product_tag') else None
        return {
            **product_data,
            # 'subcategory': subcategory_data,
            'tag': tag_data
        }


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGenderModel
        fields = '__all__'


class ProductVariantSerializer(serializers.Serializer):
    name = serializers.CharField()
    item_id = serializers.CharField()
    color = serializers.PrimaryKeyRelatedField(queryset=ColorProductModel.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=SizeProductModel.objects.all())
    percent_discount = serializers.IntegerField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    slug = serializers.SlugField(required=False)


class ProductWithVariantsSerializer(serializers.Serializer):
    extras = ProductVariantSerializer(many=True)


class VariantImageSerializer(serializers.Serializer):
    color = serializers.IntegerField()
    image = serializers.CharField()


class ProductImageGallerySerializer(serializers.Serializer):
    data = VariantImageSerializer(many=True)


class AdminProductGallerySerializer(serializers.Serializer):
    update = ProductColorImageSerializer(many=True)
    create = ProductColorImageSerializer(many=True)


class ProductWithGallerySerializer(serializers.Serializer):
    data = ProductColorImageSerializer(many=True)
