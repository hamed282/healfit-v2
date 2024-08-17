from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Max
from django.db.models import Q
from upload_path import (get_cover_image_upload_path, get_gallery_upload_path, get_description_image_upload_path,
                         get_size_table_upload_path, get_category_upload_path, get_subcategory_upload_path,
                         get_gender_upload_path, get_video_product_upload_path)
from accounts.models import User


class ProductModel(models.Model):
    objects = None
    gender = models.ForeignKey('ProductGenderModel', on_delete=models.CASCADE, related_name='gender_product', null=True, blank=True)
    product = models.CharField(max_length=100, unique=True)
    name_product = models.CharField(max_length=100, blank=True, null=True)
    cover_image = models.ImageField(upload_to=get_cover_image_upload_path, blank=True, null=True)
    cover_image_alt = models.CharField(max_length=32)
    size_table_image = models.ImageField(upload_to=get_size_table_upload_path, blank=True, null=True)
    size_table_image_alt = models.CharField(max_length=32)
    description_image = models.ImageField(upload_to=get_description_image_upload_path, blank=True, null=True)
    description_image_alt = models.CharField(max_length=32)
    price = models.CharField(max_length=8)
    percent_discount = models.IntegerField(null=True, blank=True)
    subtitle = models.CharField(max_length=256)
    application_fields = models.TextField()
    description = models.TextField()
    details = models.TextField(blank=True, null=True)
    size_guide = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=get_video_product_upload_path, blank=True, null=True)
    group_id = models.CharField(max_length=100)
    priority = models.IntegerField(blank=True, null=True, default=1)
    slug = models.SlugField(max_length=100, unique=True)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60)
    meta_description = models.CharField(max_length=150)
    schema_markup = models.TextField(null=True, blank=True)

    # Date Time Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item Groups'
        verbose_name_plural = 'Item Groups'

    def save(self, *args, **kwargs):
        # تولید اولیه slug
        original_slug = slugify(self.product)
        unique_slug = original_slug

        # بررسی و تولید slug یکتا
        num = 1
        while ProductModel.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{original_slug}-{num}'
            num += 1

        self.slug = unique_slug

        # تنظیم مقدار پیش‌فرض برای priority اگر نیاز باشد
        if self.priority is None:
            self.priority = 1

        # فراخوانی متد save پایه
        super(ProductModel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.product)

    def get_off_price(self):
        price = self.price
        percent_discount = self.percent_discount
        if self.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)

    def get_absolute_url(self):
        return f'/shop/{self.slug}'

    # @classmethod
    # def filter_products(cls, gender=None, color=None, size=None, category=None, available=None):
    #     # شروع با queryset پایه
    #     queryset = cls.objects.all()
    #
    #     # اعمال فیلترها در صورت ارائه
    #     if gender:
    #         queryset = queryset.filter(Q(gender__gender=gender) | Q(gender__gender='unisex'))
    #     if color:
    #         queryset = queryset.filter(product_color_size__color__color=color)
    #     if size:
    #         queryset = queryset.filter(product_color_size__size__size=size)
    #     if category:
    #         queryset = queryset.filter(cat_product__category__category=category)
    #     if available is not None:
    #         queryset = queryset.filter(product_color_size__quantity__gt=0 if available else 0)
    #
    #     # استفاده از distinct برای جلوگیری از تکرار
    #     return queryset.distinct()
    @classmethod
    def filter_products(cls, gender=None, color=None, size=None, category=None, subcategory=None, available=None):
        # شروع با queryset پایه برای ProductVariantModel
        variant_queryset = ProductVariantModel.objects.all()

        # اعمال فیلترها در صورت ارائه
        if color:
            variant_queryset = variant_queryset.filter(color__color=color)
        if size:
            variant_queryset = variant_queryset.filter(size__size=size)
        if available is True:
            variant_queryset = variant_queryset.filter(quantity__gt=0)

        # فیلتر کردن محصولات بر اساس واریانت‌ها
        product_ids = variant_queryset.values_list('product_id', flat=True)
        queryset = cls.objects.filter(id__in=product_ids)

        # اعمال فیلترهای بیشتر بر روی محصولات
        if gender:
            queryset = queryset.filter(Q(gender__gender=gender) | Q(gender__gender='unisex'))
        if category:
            queryset = queryset.filter(cat_product__category__category=category)
        if subcategory:
            queryset = queryset.filter(cat_product__category__category=category)

        # استفاده از distinct برای جلوگیری از تکرار
        return queryset.distinct()


class ProductVariantModel(models.Model):
    objects = None
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_color_size')
    name = models.CharField(max_length=200, unique=True)
    item_id = models.CharField(max_length=100, verbose_name='Product ID', unique=True, blank=True, null=True)
    color = models.ForeignKey('ColorProductModel', on_delete=models.CASCADE, related_name='color_product')
    size = models.ForeignKey('SizeProductModel', on_delete=models.CASCADE, related_name='size_product')
    price = models.IntegerField()
    percent_discount = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'],
                name='unique_prod_color_size_combo'
            )
        ]

        verbose_name = 'Items'
        verbose_name_plural = 'Items'

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(ProductVariantModel, self).save(**kwargs)

    def __str__(self) -> str:
        return str(self.name)

    def get_off_price(self):
        price = self.price
        percent_discount = self.percent_discount
        if self.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class ProductCategoryModel(models.Model):
    objects = None
    category = models.CharField(max_length=50)
    category_title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    image = models.FileField(upload_to=get_category_upload_path)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Category'

    def save(self, **kwargs):
        self.slug = slugify(self.category)
        super(ProductCategoryModel, self).save(**kwargs)

    def __str__(self):
        return f'{self.slug}'


class ProductSubCategoryModel(models.Model):
    objects = None
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50)
    subcategory_title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to=get_subcategory_upload_path)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Product SubCategory'
        verbose_name_plural = 'Product SubCategory'

    def save(self, **kwargs):
        self.slug = slugify(self.subcategory)
        super(ProductSubCategoryModel, self).save(**kwargs)

    def __str__(self):
        return f'{self.slug}'


class AddCategoryModel(models.Model):
    objects = None
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE, related_name='category_product')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='cat_product')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.category}'


class AddSubCategoryModel(models.Model):
    objects = None
    subcategory = models.ForeignKey(ProductSubCategoryModel, on_delete=models.CASCADE, related_name='subcategory_product')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='sub_product')

    def __str__(self):
        return f'{self.subcategory}'


class ProductGenderModel(models.Model):
    objects = None
    gender = models.CharField(max_length=50)
    gender_title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    image = models.FileField(upload_to=get_gender_upload_path)

    class Meta:
        verbose_name = 'Product Gender'
        verbose_name_plural = 'Product Gender'

    def save(self, **kwargs):
        self.slug = slugify(str(self.gender))
        super(ProductGenderModel, self).save(**kwargs)

    def __str__(self):
        return f'{self.gender}'


class ColorProductModel(models.Model):
    objects = None
    color = models.CharField(max_length=120)
    color_code = models.CharField(max_length=120)

    class Meta:
        verbose_name = 'Color Product'
        verbose_name_plural = 'Color Product'

    def __str__(self):
        return f'{self.color}'


class SizeProductModel(models.Model):
    objects = None
    size = models.CharField(max_length=120)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Size Product'
        verbose_name_plural = 'Size Products'

    def __str__(self):
        return f'{self.size}'


@receiver(pre_save, sender=ProductModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.priority is None:
        instance.priority = 1

    if instance.pk:
        existing_instance = ProductModel.objects.get(pk=instance.pk)
        current_priority = existing_instance.priority or 0
        update_priority = instance.priority or 0

        if current_priority > update_priority:
            ProductModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                priority=models.F('priority') + 1)
        elif current_priority < update_priority:
            ProductModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                priority=models.F('priority') - 1)

    elif not instance.pk:
        last_number = ProductModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if not instance.priority:
            instance.priority = (last_number or 0) + 1
        else:
            if ProductModel.objects.filter(priority__lte=instance.priority).exists():
                ProductModel.objects.filter(priority__gte=instance.priority).update(
                    priority=models.F('priority') + 1)


@receiver(pre_save, sender=SizeProductModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.pk:
        existing_instance = SizeProductModel.objects.get(pk=instance.pk)
        if not existing_instance.priority:
            last_number = SizeProductModel.objects.aggregate(max_number=Max('priority'))['max_number']
            existing_instance.priority = last_number
        else:
            current_priority = existing_instance.priority
            update_priority = instance.priority
            if current_priority > update_priority:
                SizeProductModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                    priority=models.F('priority') + 1)
            if current_priority < update_priority:
                SizeProductModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                    priority=models.F('priority') - 1)

    elif not instance.pk and not instance.priority:
        last_number = SizeProductModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if last_number:
            instance.priority = last_number + 1
        else:
            instance.priority = 1

    elif not instance.pk and instance.priority:
        if SizeProductModel.objects.filter(priority__lte=instance.priority).exists():
            SizeProductModel.objects.filter(priority__gte=instance.priority).update(
                priority=models.F('priority') + 1)


class AddImageGalleryModel(models.Model):
    objects = None
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='image_gallery_product')
    color = models.ForeignKey('ColorProductModel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_gallery_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = 'Product Image Gallery'
        verbose_name_plural = 'Product Image Gallery'

    def __str__(self):
        return f'{self.product}'


class PopularProductModel(models.Model):
    objects = None
    popular = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='popular_product')

    class Meta:
        verbose_name = 'Popular Product'
        verbose_name_plural = 'Popular Products'

    def __str__(self):
        return f'{self.popular}'


class ExtraGroupModel(models.Model):
    title = models.CharField(max_length=32)
    service_place = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.title}"


class ProductTagModel(models.Model):
    objects = None
    tag = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Product Tag'
        verbose_name_plural = 'Product Tag'

    def __str__(self):
        return f'{self.tag}'


class AddProductTagModel(models.Model):
    objects = None
    tag = models.OneToOneField(ProductTagModel, on_delete=models.CASCADE, unique=True)
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE, related_name='product_tag')

    def __str__(self):
        return f'{self.tag}'


class FavUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE)
    fav = models.BooleanField(default=False)
