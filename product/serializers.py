from rest_framework import serializers
from .models import ProductGenderModel, ProductModel, ProductVariantModel, AddImageGalleryModel, PopularProductModel


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
    gender = serializers.SlugRelatedField(read_only=True, slug_field='gender')

    class Meta:
        model = ProductModel
        fields = ['product', 'percent_discount', 'colors', 'all_size', 'size', 'cover_image', 'size_table_image',
                  'description_image', 'application_fields', 'descriptions', 'category', 'subcategory', 'gender',
                  'group_id', 'slug', 'created', 'updated', 'id', 'price']

    def get_category(self, obj):
        categories = obj.category_product.all()
        categories = [category.category.category for category in categories]
        return categories

    def get_subcategory(self, obj):
        subcategories = obj.subcategory_product.all()
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
        price = obj.price
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class ProductColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddImageGalleryModel
        fields = ['image']


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
        price = obj.price
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class ProductAllSerializer(serializers.ModelSerializer):
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
        price = obj.price
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
        price = obj.price
        percent_discount = obj.percent_discount
        if obj.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class PopularProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProductModel
        fields = ['popular']
        depth = 1
