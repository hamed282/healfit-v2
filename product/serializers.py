from rest_framework import serializers
from .models import (ProductGenderModel, ProductModel, ProductVariantModel, AddImageGalleryModel, PopularProductModel,
                     ProductCategoryModel, ProductSubCategoryModel, AddProductTagModel, AddSubCategoryModel,
                     ProductTagModel, FavUserModel, CouponModel, ProductBrandModel, CompressionClassModel, SideModel,
                     CustomMadeModel, CustomerTypeModel, ProductTypeModel, BodyAreaModel, ClassNumberModel,
                     TreatmentCategoryModel, HearAboutUsModel, CustomMadePageModel, BrandPageModel, BrandCartModel)
from django.shortcuts import get_object_or_404
import re


class ProductGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGenderModel
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrandModel
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
        size = set([f'{str(p.size)} - {str(p.size.priority)}' for p in product if p.quantity > 0])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        size = [size.split(" - ")[0] for size in sizes]
        return size

    def get_compression_class(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')

        valid_products = [p for p in product if re.search(r"/CCL.*$", p.name, re.IGNORECASE)]
        if not valid_products:
            return []
        ccl = set([f'{str(p.compression_class)} - {str(p.compression_class.priority)}' for p in product if p.quantity > 0])
        ccls = sorted(ccl, key=lambda x: int(x.split(" - ")[1]))
        ccl = [ccl.split(" - ")[0] for ccl in ccls]
        return ccl

    def get_side(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')

        valid_products = [p for p in product if re.search(r"/Side.*$", p.name, re.IGNORECASE)]
        if not valid_products:
            return []

        side = set([f'{str(p.side)} - {str(p.side.priority)}' for p in product if p.quantity > 0])
        sides = sorted(side, key=lambda x: int(x.split(" - ")[1]))
        side = [side.split(" - ")[0] for side in sides]
        return side


class GetClassSerializer(serializers.ModelSerializer):
    compression_class = serializers.SerializerMethodField()
    side = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['compression_class', 'side']

    def get_compression_class(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')

        valid_products = [p for p in product if re.search(r"/CCL.*$", p.name, re.IGNORECASE)]
        if not valid_products:
            return []
        ccl = set([f'{str(p.compression_class)} - {str(p.compression_class.priority)}' for p in product if p.quantity > 0])
        ccls = sorted(ccl, key=lambda x: int(x.split(" - ")[1]))
        ccl = [ccl.split(" - ")[0] for ccl in ccls]
        return ccl

    def get_side(self, obj):
        product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')

        valid_products = [p for p in product if re.search(r"/Side.*$", p.name, re.IGNORECASE)]
        if not valid_products:
            return []

        side = set([f'{str(p.side)} - {str(p.side.priority)}' for p in product if p.quantity > 0])
        sides = sorted(side, key=lambda x: int(x.split(" - ")[1]))
        side = [side.split(" - ")[0] for side in sides]
        return side


class NewProductSerializer(serializers.ModelSerializer):
    brand = ProductBrandSerializer()
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

    colors = serializers.SerializerMethodField()
    all_size = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    # compression_class = serializers.SerializerMethodField()
    # side = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = '__all__'

    def get_context_data(self):
        compression_class = self.context.get('compression_class', None)
        side = self.context.get('side', None)

        if compression_class == "":
            compression_class = None
        else:
            compression_class = CompressionClassModel.objects.filter(compression_class=compression_class).first()

        if side == "":
            side = None
        else:
            side = SideModel.objects.filter(side=side).first()

        return compression_class, side

    def get_colors(self, obj):
        compression_class, side = self.get_context_data()

        product = ProductVariantModel.objects.filter(product=obj,
                                                     compression_class=compression_class,
                                                     side=side)

        colors = set([f'{str(p.color.color)} - {str(p.color.color_code)} - {str(p.color.id)}' for p in product])
        all_colors = [{'color': color.split(" - ")[0], 'code': color.split(" - ")[1], 'id': color.split(" - ")[2]} for color in colors]
        return all_colors

    def get_all_size(self, obj):
        compression_class, side = self.get_context_data()

        product = ProductVariantModel.objects.filter(product=obj, compression_class=compression_class, side=side)
        size = set([f'{str(p.size)} - {str(p.size.priority)} - {str(p.size.id)}' for p in product])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        all_size = [{'size': size.split(" - ")[0], 'id': size.split(" - ")[1]} for size in sizes]
        return all_size

    def get_size(self, obj):
        compression_class, side = self.get_context_data()

        product = ProductVariantModel.objects.filter(product=obj, compression_class=compression_class, side=side)
        size = set([f'{str(p.size)} - {str(p.size.priority)}' for p in product if p.quantity > 0])
        sizes = sorted(size, key=lambda x: int(x.split(" - ")[1]))
        size = [size.split(" - ")[0] for size in sizes]
        return size

    # def get_compression_class(self, obj):
    #     product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
    #
    #     valid_products = [p for p in product if re.search(r"/CCL.*$", p.name, re.IGNORECASE)]
    #     if not valid_products:
    #         return []
    #     ccl = set([f'{str(p.compression_class)} - {str(p.compression_class.priority)}' for p in product if p.quantity > 0])
    #     ccls = sorted(ccl, key=lambda x: int(x.split(" - ")[1]))
    #     ccl = [ccl.split(" - ")[0] for ccl in ccls]
    #     return ccl
    #
    # def get_side(self, obj):
    #     product = ProductVariantModel.objects.filter(product=obj)  # .order_by('-priority')
    #
    #     valid_products = [p for p in product if re.search(r"/Side.*$", p.name, re.IGNORECASE)]
    #     if not valid_products:
    #         return []
    #
    #     side = set([f'{str(p.side)} - {str(p.side.priority)}' for p in product if p.quantity > 0])
    #     sides = sorted(side, key=lambda x: int(x.split(" - ")[1]))
    #     side = [side.split(" - ")[0] for side in sides]
    #     return side

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
                  'quantity', 'size', 'color', 'item_id', 'slug', 'id', 'compression_class', 'side']

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
                  'percent_discount', 'group_id', 'slug', 'subtitle', 'is_best_seller']

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
        fields = ['id', 'name_product', 'gender', 'category', 'subcategory', 'product', 'cover_image', 'price',
                  'percent_discount', 'group_id', 'slug', 'subtitle', 'fav', 'size_table_image_alt', 'cover_image_alt',
                  'description_image_alt', 'off_price', 'is_active', 'is_best_seller']

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
        fields = ['product', 'price', 'off_price', 'slug', 'group_id', 'id', 'is_best_seller']

    def get_off_price(self, obj):
        price = int(float(obj.price))
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
    category_name = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()

    class Meta:
        model = ProductSubCategoryModel
        fields = '__all__'

    def get_category_name(self, obj):
        return obj.category.category_title

    def get_category_slug(self, obj):
        return obj.category.slug


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
        product = self.context['product_id']
        return FavUserModel.objects.create(user=user,
                                           product=ProductModel.objects.get(id=product),
                                           **validated_data)


class UserFavSerializer(serializers.ModelSerializer):
    user_fav = ProductAllSerializer(source='product', read_only=True)

    class Meta:
        model = FavUserModel
        fields = ['user_fav']


class ProductCartSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(read_only=True, slug_field='product')
    size = serializers.SlugRelatedField(read_only=True, slug_field='size')
    color = serializers.SlugRelatedField(read_only=True, slug_field='color')
    off_price = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    max_quantity = serializers.IntegerField(source='quantity', read_only=True)

    class Meta:
        model = ProductVariantModel
        fields = ['id', 'product', 'price', 'off_price', 'size', 'color', 'gender', 'cover_image', 'max_quantity']

    def get_gender(self, obj):
        try:
            gender = obj.product.gender.gender
        except:
            gender = None
        return gender

    def get_cover_image(self, obj):
        product = AddImageGalleryModel.objects.filter(product=obj.product, color=obj.color).first()
        try:
            cover = product.image.url
        except:
            cover = None
        return cover


    def get_off_price(self, obj):
        price = int(obj.price)
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class QuantityProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariantModel
        fields = ['quantity']


class CouponSerializer(serializers.ModelSerializer):
    # customer = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    expire = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CouponModel
        fields = '__all__'


class CouponCreateSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CouponModel
        fields = '__all__'

    def get_products(self, obj):
        return 'products'


class CategoryBestSellerSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    category_title = serializers.CharField()
    best_seller_products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategoryModel
        fields = ['category', 'category_title', 'best_seller_products', 'slug']

    def get_best_seller_products(self, obj):
        best_seller_products = []
        products = obj.category_product.filter(product__is_best_seller=True)
        for product in products:
            product_data = ProductAllSerializer(product.product, context=self.context).data
            best_seller_products.append(product_data)
        return best_seller_products


class CustomMadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMadeModel
        fields = '__all__'


class CustomerTypeSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='customer_type')
    
    class Meta:
        model = CustomerTypeModel
        fields = ['id', 'value']


class ProductTypeSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='product_type')
    
    class Meta:
        model = ProductTypeModel
        fields = ['id', 'value']


class BodyAreaSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='body_area')
    
    class Meta:
        model = BodyAreaModel
        fields = ['id', 'value']


class ClassNumberSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='class_num')
    
    class Meta:
        model = ClassNumberModel
        fields = ['id', 'value']


class TreatmentCategorySerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='treatment_category')
    
    class Meta:
        model = TreatmentCategoryModel
        fields = ['id', 'value']


class HearAboutUsSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='hear_about_us')
    
    class Meta:
        model = HearAboutUsModel
        fields = ['id', 'value']


class CustomMadeOptionsSerializer(serializers.Serializer):
    customer_types = CustomerTypeSerializer(many=True, read_only=True)
    product_types = ProductTypeSerializer(many=True, read_only=True)
    body_areas = BodyAreaSerializer(many=True, read_only=True)
    class_numbers = ClassNumberSerializer(many=True, read_only=True)
    treatment_categories = TreatmentCategorySerializer(many=True, read_only=True)
    hear_about_us_options = HearAboutUsSerializer(many=True, read_only=True)


class CustomMadePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMadePageModel
        fields = '__all__'


class BrandPageSerializer(serializers.ModelSerializer):
    brand = ProductBrandSerializer()
    
    class Meta:
        model = BrandPageModel
        fields = '__all__'


class BrandCartSerializer(serializers.ModelSerializer):
    brand = ProductBrandSerializer()
    
    class Meta:
        model = BrandCartModel
        fields = '__all__'
