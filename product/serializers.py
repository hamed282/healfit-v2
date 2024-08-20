from rest_framework import serializers
from .models import (ProductGenderModel, ProductModel, ProductVariantModel, AddImageGalleryModel, PopularProductModel,
                     ProductCategoryModel, ProductSubCategoryModel, AddProductTagModel, AddSubCategoryModel,
                     ProductTagModel, FavUserModel)
from django.shortcuts import get_object_or_404


class ProductGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGenderModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    all_size = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    gender = serializers.SlugRelatedField(read_only=True, slug_field='id')
    tag = serializers.SerializerMethodField()
    price = serializers.FloatField()
    group_id = serializers.IntegerField()
    name_product = serializers.CharField(required=False, allow_null=True)

    cover_image = serializers.ImageField(required=False, allow_null=True)
    size_table_image = serializers.ImageField(required=False, allow_null=True)
    description_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = ProductModel
        fields = '__all__'

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
        size = set([f'{str(p.size)} - {str(p.size.priority)}' for p in product if p.quantity > 0])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        size = [size.split(" - ")[0] for size in sizes]
        return size


class ProductAdminSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    all_size = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    gender = serializers.SlugRelatedField(read_only=True, slug_field='id')
    tag = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = '__all__'

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

        colors = set([f'{str(p.color.color)} - {str(p.color.color_code)}' for p in product])
        all_colors = [{'color': color.split(" - ")[0], 'code': color.split(" - ")[1]} for color in colors]
        return all_colors

    def get_all_size(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
        size = set([f'{str(p.size)} - {str(p.size.priority)}' for p in product])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        all_size = [size.split(" - ")[0] for size in sizes]
        return all_size

    def get_size(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
        size = set([f'{str(p.size)} - {str(p.size.priority)}' for p in product if p.quantity > 0])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        size = [size.split(" - ")[0] for size in sizes]
        return size


class ProductVariantShopSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(read_only=True, slug_field='product')
    size = serializers.SlugRelatedField(read_only=True, slug_field='size')
    color = serializers.SlugRelatedField(read_only=True, slug_field='color')
    off_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariantModel
        fields = ['product', 'name', 'price', 'off_price', 'percent_discount',
                  'quantity', 'size', 'color', 'item_id', 'slug', 'id']

    def get_off_price(self, obj):
        price = int(obj.price)
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class ProductColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddImageGalleryModel
        fields = '__all__'


class ProductColorImageListSerializer(serializers.Serializer):
    images = ProductColorImageSerializer(many=True)


class ColorSizeProductSerializer(serializers.ModelSerializer):
    color = serializers.SlugRelatedField(read_only=True, slug_field='color')
    color_code = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariantModel
        fields = ['color', 'quantity', 'id', 'color_code']

    def get_color_code(self, obj):
        return obj.color.color_code


class ProductListSerializer(serializers.ModelSerializer):
    gender = serializers.SlugRelatedField(slug_field='gender', read_only=True)
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    off_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['gender', 'category', 'subcategory', 'product', 'cover_image', 'price', 'off_price',
                  'percent_discount', 'group_id', 'slug', 'subtitle']

    def get_category(self, obj):
        categories = obj.category_product.all()
        categories = [category.category.category for category in categories]

        return categories

    def get_subcategory(self, obj):
        subcategories = obj.subcategory_product.all()
        subcategories = [subcategory.subcategory.subcategory for subcategory in subcategories]

        return subcategories

    def get_off_price(self, obj):
        price = int(obj.price)
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class ProductAllSerializer(serializers.ModelSerializer):
    gender = serializers.SlugRelatedField(slug_field='gender', read_only=True)
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    off_price = serializers.SerializerMethodField()
    fav = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['id', 'gender', 'category', 'subcategory', 'product', 'cover_image', 'price', 'off_price',
                  'percent_discount', 'group_id', 'slug', 'subtitle', 'fav']

    def get_fav(self, obj):
        request = self.context.get('request', None)

        if request and request.user.is_authenticated:
            fav = FavUserModel.objects.filter(user=request.user, product=obj).exists()
        else:
            fav = False

        return fav

    def get_category(self, obj):
        categories = obj.cat_product.all()
        categories = [category.category.category for category in categories]

        return categories

    def get_subcategory(self, obj):
        subcategories = obj.sub_product.all()
        subcategories = [subcategory.subcategory.subcategory for subcategory in subcategories]

        return subcategories

    def get_off_price(self, obj):
        price = float(obj.price)
        price = int(price)
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class ProductSearchSerializer(serializers.ModelSerializer):
    off_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['product', 'price', 'off_price', 'slug', 'group_id', 'id']

    def get_off_price(self, obj):
        price = int(obj.price)
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class PopularProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProductModel
        fields = ['popular']
        depth = 1


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubCategoryModel
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    subcategories = ProductSubCategorySerializer(many=True, read_only=True, source='productsubcategorymodel_set')

    class Meta:
        model = ProductCategoryModel
        fields = '__all__'


class ProductByCategorySerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    off_price = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.product.id

    def get_product(self, obj):
        return obj.product.product

    def get_cover_image(self, obj):
        if obj.product.cover_image:
            return obj.product.cover_image.url
        return None

    def get_off_price(self, obj):
        product = obj.product
        price = int(product.price)
        percent_discount = product.percent_discount
        if percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)

    def get_slug(self, obj):
        return obj.product.slug


class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class AddSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddSubCategoryModel
        fields = '__all__'


class AddProductTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(write_only=True)

    class Meta:
        model = AddProductTagModel
        fields = ['product', 'tag_name']

    def create(self, validated_data):
        tag_name = validated_data.pop('tag_name')
        tag, created = ProductTagModel.objects.get_or_create(tag=tag_name)
        validated_data['tag'] = tag
        return super().create(validated_data)

    def update(self, instance, validated_data):
        tag_name = validated_data.pop('tag_name', None)
        if tag_name:
            tag, created = ProductTagModel.objects.get_or_create(tag=tag_name)
            instance.tag = tag
        return super().update(instance, validated_data)


class FavProductSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(read_only=True, slug_field='product')

    class Meta:
        model = FavUserModel
        exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        return FavUserModel.objects.create(user=user, **validated_data)


# class FavUserSerializer(serializers.Serializer):
#     product = ProductSerializer(many=True)