from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from accounts.models import User, RoleUserModel, RoleModel
from blog.models import (BlogTagModel, AddBlogTagModel, BlogCategoryModel, BlogModel, CommentBlogModel,
                         AddCategoryModel as AddBlogCategoryModel, AuthorBlogModel)
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from product.models import (ExtraGroupModel, SizeProductModel, ColorProductModel, AddImageGalleryModel, ProductTagModel,
                            ProductSubCategoryModel, ProductModel, AddProductTagModel, ProductGenderModel,
                            AddSubCategoryModel, ProductVariantModel, AddCategoryModel, ProductCategoryModel,
                            CustomerTypeModel, ProductTypeModel, BodyAreaModel, ClassNumberModel,
                            TreatmentCategoryModel, HearAboutUsModel, CompressionClassModel, SideModel,
                            ProductBrandModel, BrandCartImageModel, BrandCartModel)
from product.serializers import ProductColorImageSerializer, ProductBrandSerializer
from order.models import OrderItemModel, OrderModel, OrderStatusModel, ShippingModel, ShippingCountryModel
import re


class UserSerializer(ModelSerializer):
    role = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active']

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


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


class RoleUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('role',)


class RoleSerializer(ModelSerializer):
    class Meta:
        model = RoleModel
        fields = '__all__'


class AddRoleSerializer(ModelSerializer):
    class Meta:
        model = RoleUserModel
        fields = '__all__'


class LoginUserSerializer(ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']

    def get_role(self, obj):
        try:
            role = RoleUserModel.objects.get(user=obj)
            role = role.role.role
        except:
            role = 'user'
        return role


class BlogTagSerializer(ModelSerializer):
    class Meta:
        model = BlogTagModel
        fields = '__all__'


class BlogCategorySerializer(ModelSerializer):
    canonical = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    meta_title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    meta_description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

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
    cover_image_alt = serializers.CharField(max_length=125)
    title = serializers.CharField(max_length=250)
    short_description = serializers.CharField(max_length=160)
    body = serializers.CharField()
    is_active = serializers.BooleanField()
    slug = serializers.SlugField()
    follow = serializers.BooleanField(default=False)
    index = serializers.BooleanField(default=False)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_blank=True)
    schema_markup = serializers.CharField(required=False, allow_blank=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_blank=True)
    tag = serializers.PrimaryKeyRelatedField(queryset=BlogTagModel.objects.all(), required=False, allow_null=True)
    categories = serializers.CharField(required=False, allow_blank=True)
    read_duration = serializers.CharField(max_length=16, required=False, allow_blank=True)
    author = serializers.PrimaryKeyRelatedField(queryset=AuthorBlogModel.objects.all(), required=False, allow_null=True)

    def create(self, validated_data):
        # Extract tag and categories data
        tag = validated_data.pop('tag', None)
        categories_str = validated_data.pop('categories', '')

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

        # Create AddCategoryModel instances for each category
        if categories_str:
            categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
            for category_name in categories:
                try:
                    category = BlogCategoryModel.objects.get(category=category_name)
                except BlogCategoryModel.DoesNotExist:
                    category = BlogCategoryModel.objects.create(
                        category=category_name,
                        slug=slugify(category_name)
                    )
                AddBlogCategoryModel.objects.create(blog=blog, category=category)

        return blog

    def update(self, instance, validated_data):
        tag = validated_data.pop('tag', None)
        categories_str = validated_data.pop('categories', '')

        # Update BlogModel instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update AddBlogTagModel if tag is provided
        if tag:
            AddBlogTagModel.objects.update_or_create(blog=instance, defaults={'tag': tag})
        elif hasattr(instance, 'blog_tag'):
            instance.blog_tag.delete()

        # Update categories
        if categories_str:
            # Delete existing categories
            AddBlogCategoryModel.objects.filter(blog=instance).delete()
            # Create new category associations
            categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
            for category_name in categories:
                try:
                    category = BlogCategoryModel.objects.get(category=category_name)
                except BlogCategoryModel.DoesNotExist:
                    category = BlogCategoryModel.objects.create(
                        category=category_name,
                        slug=slugify(category_name)
                    )
                AddBlogCategoryModel.objects.create(blog=instance, category=category)

        return instance

    def to_representation(self, instance):
        blog_data = BlogModelSerializer(instance).data
        category_data = [cat.category.category for cat in instance.cat_blog.all()]
        tag_data = AddBlogTagSerializer(instance.blog_tag).data if hasattr(instance, 'blog_tag') else None
        return {**blog_data, 'categories': ','.join(category_data), 'tag': tag_data['tag'] if tag_data else None}


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


class ProductSerializer(serializers.ModelSerializer):
    brand = ProductBrandSerializer()
    colors = serializers.SerializerMethodField()
    all_size = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    compression_class = serializers.SerializerMethodField()
    side = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    gender = serializers.SlugRelatedField(read_only=True, slug_field='id')
    gender_data = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    price = serializers.FloatField()
    off_price = serializers.SerializerMethodField()
    group_id = serializers.IntegerField()
    name_product = serializers.CharField(required=False, allow_null=True)
    video = serializers.FileField(required=False, allow_null=True)
    percent_discount = serializers.IntegerField(required=False, allow_null=True)
    schema_markup = serializers.CharField(required=False, allow_null=True)

    cover_image = serializers.ImageField(required=False, allow_null=True)
    size_table_image = serializers.ImageField(required=False, allow_null=True)
    description_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = ProductModel
        fields = '__all__'

    def get_off_price(self, obj):
        price = float(obj.price)
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)

    def get_gender_data(self, obj):
        if obj.gender is not None:
            gender_name = obj.gender.gender
            gender_slug = obj.gender.slug
        else:
            gender_name = None
            gender_slug = None
        return {'gender_name': gender_name, 'gender_slug': gender_slug}

    def get_tag(self, product):
        try:
            tag = AddProductTagModel.objects.get(product=product)
            tag = tag.tag.tag
        except:
            tag = None
        return tag

    def get_category(self, obj):
        categories = obj.cat_product.all()
        categories = [category.category.category for category in categories]
        return categories

    def get_subcategory(self, obj):
        subcategories = obj.sub_product.all()
        subcategories = [subcategory.subcategory.subcategory for subcategory in subcategories]
        return subcategories

    def get_colors(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)

        colors = set([f'{str(p.color.color)} - {str(p.color.color_code)} - {str(p.color.id)}' for p in product])
        all_colors = [{'color': color.split(" - ")[0], 'code': color.split(" - ")[1], 'id': color.split(" - ")[2]} for color in colors]
        return all_colors

    def get_all_size(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
        size = set([f'{str(p.size)} - {str(p.size.priority)} - {str(p.size.id)}' for p in product])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        all_size = [{'size': size.split(" - ")[0], 'id': size.split(" - ")[1]} for size in sizes]
        return all_size

    def get_size(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
        size = set([f'{str(p.size)}' for p in product])

        return size

    def get_compression_class(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
        try:
            ccls = set([f'{str(p.compression_class)} - {str(p.compression_class.id)}' for p in product])
            ccl = [{'compression_class': ccl.split(" - ")[0], 'id': ccl.split(" - ")[1]} for ccl in ccls]
        except:
            ccl = None

        return ccl

    def get_side(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
        try:
            sides = set([f'{str(p.side)} - {str(p.side.id)}' for p in product])
            side = [{'side': side.split(" - ")[0], 'id': side.split(" - ")[1]} for side in sides]
        except:
            side = None

        return side


class CombinedProductSerializer(serializers.Serializer):
    gender = serializers.PrimaryKeyRelatedField(queryset=ProductGenderModel.objects.all(), required=False, allow_null=True)
    product = serializers.CharField(required=False, allow_null=True)
    name_product = serializers.CharField(required=False, allow_null=True)
    description_image = serializers.ImageField(required=False, allow_null=True)
    description_image_alt = serializers.CharField(required=False, allow_null=True)
    size_table_image = serializers.ImageField(required=False, allow_null=True)
    size_table_image_alt = serializers.CharField(required=False, allow_null=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    cover_image_alt = serializers.CharField(required=False, allow_null=True)
    video = serializers.FileField(required=False, allow_null=True)
    price = serializers.CharField(required=False, allow_null=True)
    percent_discount = serializers.IntegerField(required=False, allow_null=True)
    subtitle = serializers.CharField(required=False, allow_null=True)
    application_fields = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    details = serializers.CharField(required=False, allow_null=True)
    size_guide = serializers.CharField(required=False, allow_null=True)
    group_id = serializers.CharField(required=False, allow_null=True)
    priority = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.BooleanField(default=False)
    is_best_seller = serializers.BooleanField(default=False)
    slug = serializers.SlugField(required=False, allow_null=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=ProductBrandModel.objects.all(), required=False, allow_null=True)

    category = serializers.CharField(required=False, allow_null=True)
    subcategory = serializers.CharField(required=False, allow_null=True)
    follow = serializers.BooleanField(default=False)
    index = serializers.BooleanField(default=False)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_null=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_null=True)
    schema_markup = serializers.CharField(required=False, allow_null=True)
    tag_name = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def create(self, validated_data):
        # Extract and process tag data
        tag_name = validated_data.pop('tag_name', None)
        tag = None
        if tag_name:
            tag, created = ProductTagModel.objects.get_or_create(tag=tag_name)

        # Generate unique slug
        slug = validated_data['slug']
        if slug is None:
            validated_data['slug'] = None
        else:
            validated_data['slug'] = slug

        subcategory_name = validated_data.pop('subcategory', None)
        category_name = validated_data.pop('category', None)
        # Create ProductModel instance
        product = ProductModel.objects.create(**validated_data)

        if subcategory_name is not None:
            subcategory_name = subcategory_name.split(',')
        else:
            subcategory_name = []
        for sub in subcategory_name:
            subcategory = get_object_or_404(ProductSubCategoryModel, subcategory=sub)
            # Create AddSubCategoryModel instance
            AddSubCategoryModel.objects.create(product=product, subcategory=subcategory)

            # category = subcategory.category
            # if not AddCategoryModel.objects.filter(product=product, category=category).exists():
            #     AddCategoryModel.objects.create(product=product, category=category)

        if category_name is not None:
            category_name = category_name.split(',')
        else:
            category_name = []
        for cat in category_name:
            category = get_object_or_404(ProductCategoryModel, category=cat)
            # Create AddSubCategoryModel instance
            AddCategoryModel.objects.create(product=product, category=category)

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
        category_name = validated_data.pop('category', None)
        product_id = self.context.get('product_id', None)

        product = ProductModel.objects.get(id=product_id)
        
        if subcategory_name is not None:
            subcategory_name = subcategory_name.split(',')
        else:
            subcategory_name = []
        if len(subcategory_name) > 0:
            add_sub = AddSubCategoryModel.objects.filter(product=product)

            add_sub.delete()
            for sub in subcategory_name:

                subcategory = get_object_or_404(ProductSubCategoryModel, subcategory=sub)
                # Create AddSubCategoryModel instance
                AddSubCategoryModel.objects.create(product=product, subcategory=subcategory)

        if category_name is not None:
            category_name = category_name.split(',')
        else:
            category_name = []
        if len(category_name) > 0:
            add_cat = AddCategoryModel.objects.filter(product=product)

            add_cat.delete()
            for cat in category_name:

                category = get_object_or_404(ProductCategoryModel, category=cat)
                # Create AddSubCategoryModel instance
                AddCategoryModel.objects.create(product=product, category=category)

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

        try:
            variants = ProductVariantModel.objects.filter(product=product)
            discount = validated_data.pop('percent_discount', 0)
            for variant in variants:
                variant.percent_discount = discount
                variant.save()
        except:
            pass

        return instance

    def to_representation(self, instance):
        product_data = ProductSerializer(instance).data
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
    side = serializers.PrimaryKeyRelatedField(queryset=SideModel.objects.all(), required=False, allow_null=True)
    compression_class = serializers.PrimaryKeyRelatedField(queryset=CompressionClassModel.objects.all(), required=False, allow_null=True)
    percent_discount = serializers.IntegerField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    slug = serializers.SlugField(required=False)
    id = serializers.IntegerField()


class ProductWithVariantsSerializer(serializers.Serializer):
    extras = ProductVariantSerializer(many=True)


class ColorImageSerializer(serializers.ModelSerializer):
    # color = serializers.SlugRelatedField(read_only=True, slug_field='color')
    color = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariantModel
        fields = ['color']

    def get_color(self, obj):
        return 'color'


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


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='first_name')
    status = serializers.SlugRelatedField(read_only=True, slug_field='status')
    number_of_products = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'user', 'status', 'paid', 'created', 'amount', 'number_of_products', 'transaction_ref']

    def get_amount(self, obj):
        items = OrderItemModel.objects.filter(order=obj)
        total_price = 0
        for item in items:
            price = item.price*item.quantity
            total_price += price
        return total_price

    def get_number_of_products(self, obj):
        items = len(OrderItemModel.objects.filter(order=obj))
        return items


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='first_name')
    status = serializers.SlugRelatedField(slug_field='status', queryset=OrderStatusModel.objects.all())
    address = serializers.SlugRelatedField(read_only=True, slug_field='address')
    number_of_products = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = OrderModel
        fields = '__all__'

    def get_coupon(self, obj):
        if obj.coupon:
            return f'{obj.coupon.customer} - {obj.coupon.coupon_code}'
        return None

    def get_amount(self, obj):
        items = OrderItemModel.objects.filter(order=obj)
        total_price = 0
        for item in items:
            price = item.price*item.quantity
            total_price += price
        return total_price

    def get_number_of_products(self, obj):
        items = len(OrderItemModel.objects.filter(order=obj))
        return items

    def to_internal_value(self, data):
        # ایجاد یک نسخه کپی از داده‌ها
        mutable_data = data.copy()

        status_value = mutable_data.get('status')

        # سعی می‌کنیم فیلد status را از طریق مقدار slug_field پیدا کنیم
        if status_value:
            try:
                status_instance = OrderStatusModel.objects.get(status=status_value)
                mutable_data['status'] = status_instance
            except OrderStatusModel.DoesNotExist:
                raise serializers.ValidationError({"status": "Status with this value does not exist."})

        return super().to_internal_value(mutable_data)


class OrderItemSerializer(serializers.ModelSerializer):
    size = serializers.SlugRelatedField(slug_field='size', read_only=True)
    color = serializers.SlugRelatedField(slug_field='color', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', 'image', 'price', 'size', 'color', 'quantity', 'total_price']

    def get_image(self, obj):
        product = obj.product.product
        image = product.cover_image
        if image == '':
            image = 'None'
        else:
            image = image.url
        return image

    def get_total_price(self, obj):
        total_price = obj.price * obj.quantity
        return total_price


class CommentBlogSerializer(ModelSerializer):
    blog = serializers.SlugRelatedField(read_only=True, slug_field='title')

    class Meta:
        model = CommentBlogModel
        fields = '__all__'


class ShippingCountrySerializer(ModelSerializer):
    class Meta:
        model = ShippingCountryModel
        fields = '__all__'


class CityShippingSerializer(ModelSerializer):
    class Meta:
        model = ShippingModel
        fields = '__all__'


class ShippingSerializer(ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = ShippingCountryModel
        fields = '__all__'

    def get_city(self, obj):
        cities = ShippingModel.objects.filter(country=obj)
        data = [{'id': city.id, 'city': city.city, 'threshold_free': city.threshold_free,
                 'shipping_fee': city.shipping_fee, 'delivery_day': city.delivery_day} for city in cities]
        return data


class BlogAuthorSerializer(ModelSerializer):
    canonical = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    meta_title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    meta_description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = AuthorBlogModel
        fields = '__all__'


class CustomerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerTypeModel
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTypeModel
        fields = '__all__'


class BodyAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BodyAreaModel
        fields = '__all__'


class ClassNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassNumberModel
        fields = '__all__'


class TreatmentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TreatmentCategoryModel
        fields = '__all__'


class HearAboutUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HearAboutUsModel
        fields = '__all__'


class CompressionClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompressionClassModel
        fields = '__all__'


class SideSerializer(serializers.ModelSerializer):

    class Meta:
        model = SideModel
        fields = '__all__'


class BrandCartImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandCartImageModel
        fields = ['id', 'image', 'image_alt', 'priority']


class BrandCartSerializer(serializers.ModelSerializer):
    images = BrandCartImageSerializer(many=True)

    class Meta:
        model = BrandCartModel
        fields = ['id', 'content', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        brand_cart = BrandCartModel.objects.create(**validated_data)
        for image_data in images_data:
            BrandCartImageModel.objects.create(brand_cart=brand_cart, **image_data)
        return brand_cart


class ProductBrandCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductBrandModel
        fields = ['id', 'brand', 'brand_logo', 'brand_logo_alt', 'slug',
                  'image_desktop', 'image_mobile', 'image_alt',
                  'content1_title', 'content1_image', 'content1_image_alt', 'content1_text',
                  'content2_text', 'content2_right_image', 'content2_right_image_alt', 'content2_right',
                  'content2_mid_image', 'content2_mid_image_alt', 'content2_mid',
                  'content2_left_image', 'content2_left_image_alt', 'content2_left',
                  'contact_image', 'contact_image_alt', 'contact_text']
        extra_kwargs = {
            'image': {'required': False},
        }

    def create(self, validated_data):
        brand_carts_data = validated_data.pop('brand_carts', [])

        brand = super().create(validated_data)

        request = self.context.get('request')
        if brand_carts_data and request:
            for i, cart in enumerate(brand_carts_data):
                images = cart.pop('images', [])
                brand_cart = BrandCartModel.objects.create(brand=brand, content=cart.get('content', ''))

                for j, image_info in enumerate(images):
                    image_field = f'brand_carts[{i}].images[{j}].image'
                    image_file = request.FILES.get(image_field)

                    BrandCartImageModel.objects.create(
                        brand_cart=brand_cart,
                        image=image_file,
                        image_alt=image_info.get('image_alt'),
                        priority=image_info.get('priority'),
                    )
        return brand


class ProductBrandUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductBrandModel
        fields = '__all__'

    def update(self, instance, validated_data):
        brand_carts_data = validated_data.pop('brand_carts', [])

        # به‌روزرسانی فیلدهای اصلی برند
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # کارت‌های موجود این برند
        existing_cart_ids = [cart.id for cart in instance.brandcartmodel_set.all()]

        # پیگیری کارت‌هایی که کاربر فرستاده
        sent_cart_ids = []

        for cart_data in brand_carts_data:
            images_data = cart_data.pop('images', [])
            cart_id = cart_data.get('id', None)

            if cart_id and BrandCartModel.objects.filter(id=cart_id, brand=instance).exists():
                cart = BrandCartModel.objects.get(id=cart_id, brand=instance)
                for attr, value in cart_data.items():
                    setattr(cart, attr, value)
                cart.save()
                sent_cart_ids.append(cart.id)
            else:
                cart = BrandCartModel.objects.create(brand=instance, **cart_data)
                sent_cart_ids.append(cart.id)

            # بروزرسانی تصاویر مربوط به کارت
            existing_image_ids = [img.id for img in cart.images.all()]
            sent_image_ids = []

            for image_data in images_data:
                image_id = image_data.get('id', None)
                if image_id and BrandCartImageModel.objects.filter(id=image_id, brand_cart=cart).exists():
                    image = BrandCartImageModel.objects.get(id=image_id, brand_cart=cart)
                    for attr, value in image_data.items():
                        setattr(image, attr, value)
                    image.save()
                    sent_image_ids.append(image.id)
                else:
                    image = BrandCartImageModel.objects.create(brand_cart=cart, **image_data)
                    sent_image_ids.append(image.id)

            # حذف تصاویر حذف‌شده
            BrandCartImageModel.objects.filter(brand_cart=cart).exclude(id__in=sent_image_ids).delete()

        # حذف کارت‌های حذف‌شده
        BrandCartModel.objects.filter(brand=instance).exclude(id__in=sent_cart_ids).delete()

        return instance


class BrandSerializer(serializers.ModelSerializer):
    brand_carts = BrandCartSerializer(source='brandcartmodel_set', many=True, read_only=True)

    class Meta:
        model = ProductBrandModel
        fields = '__all__'
