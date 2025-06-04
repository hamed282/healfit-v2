from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Max
from django.db.models import Q
from upload_path import (get_cover_image_upload_path, get_gallery_upload_path, get_description_image_upload_path,
                         get_size_table_upload_path, get_category_upload_path, get_subcategory_upload_path,
                         get_gender_upload_path, get_video_product_upload_path, get_brand_logo_upload_path,
                         get_custom_made_upload_path, get_brand_upload_path, get_brand_cart_upload_path,
                         get_attach_file_upload_path)
from accounts.models import User
from django.utils import timezone


class ProductModel(models.Model):
    objects = None
    gender = models.ForeignKey('ProductGenderModel', on_delete=models.CASCADE, related_name='gender_product', null=True, blank=True)
    product = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey('ProductBrandModel', on_delete=models.CASCADE, null=True, blank=True)
    name_product = models.CharField(max_length=100, blank=True, null=True)
    cover_image = models.ImageField(upload_to=get_cover_image_upload_path, blank=True, null=True)
    cover_image_alt = models.CharField(max_length=256, blank=True, null=True)
    size_table_image = models.ImageField(upload_to=get_size_table_upload_path, blank=True, null=True)
    size_table_image_alt = models.CharField(max_length=256, blank=True, null=True)
    description_image = models.ImageField(upload_to=get_description_image_upload_path, blank=True, null=True)
    description_image_alt = models.CharField(max_length=256, blank=True, null=True)
    price = models.CharField(max_length=8)
    percent_discount = models.IntegerField(null=True, blank=True)
    subtitle = models.CharField(max_length=256, blank=True, null=True)
    application_fields = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, default='')
    details = models.TextField(blank=True, null=True, default='')
    size_guide = models.TextField(blank=True, null=True, default='')
    video = models.FileField(upload_to=get_video_product_upload_path, blank=True, null=True)
    group_id = models.CharField(max_length=100)
    is_best_seller = models.BooleanField(default=False)
    priority = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    # Date Time Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item Groups'
        verbose_name_plural = 'Item Groups'

    def save(self, *args, **kwargs):
        if self.slug is None:
            original_slug = slugify(self.product)
            unique_slug = original_slug

            num = 1
            while ProductModel.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1

            self.slug = unique_slug

        if self.priority is None:
            last_priority = ProductModel.objects.count()
            self.priority = last_priority + 1

        super(ProductModel, self).save(*args, **kwargs)

        # به‌روز رسانی priority برای از بین بردن فاصله‌ها
        all_products = ProductModel.objects.all().order_by('priority')
        for index, product in enumerate(all_products, start=1):
            if product.priority != index:
                product.priority = index
                product.save(update_fields=['priority'])

    def __str__(self) -> str:
        return str(self.product)

    def get_off_price(self):
        price = float(self.price)
        percent_discount = self.percent_discount
        if self.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)

    def get_absolute_url(self):
        return f'/shop/{self.slug}'

    @classmethod
    def filter_products(cls, gender=None, color=None, size=None, category=None, subcategory=None, available=None,
                        compression_class=None, side=None):
        # شروع با queryset پایه برای ProductVariantModel
        variant_queryset = ProductVariantModel.objects.all()

        # اعمال فیلترها در صورت ارائه
        if color:
            variant_queryset = variant_queryset.filter(color__color__in=color)
        if size:
            variant_queryset = variant_queryset.filter(size__size__in=size)
        if available is True:
            variant_queryset = variant_queryset.filter(quantity__gt=0)
        if side:
            variant_queryset = variant_queryset.filter(side__side__in=side)
        if compression_class:
            variant_queryset = variant_queryset.filter(compression_class__compression_class__in=compression_class)

        # فیلتر کردن محصولات بر اساس واریانت‌ها
        product_ids = variant_queryset.values_list('product_id', flat=True)
        queryset = cls.objects.filter(id__in=product_ids, is_active=True)

        if gender:
            if gender in ["male", "female"]:
                queryset = queryset.filter(Q(gender__gender=gender) | Q(gender__gender="unisex"))
            else:
                queryset = queryset.filter(gender__gender=gender)
        if category:
            queryset = queryset.filter(cat_product__category__category=category)
        if subcategory:
            queryset = queryset.filter(sub_product__subcategory__subcategory=subcategory)

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
    compression_class = models.ForeignKey('CompressionClassModel', on_delete=models.CASCADE, blank=True, null=True)
    side = models.ForeignKey('SideModel', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size', 'compression_class', 'side'],
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
        price = float(self.price)
        percent_discount = self.percent_discount
        if self.percent_discount is None:
            percent_discount = 0
        return int(price - price * percent_discount / 100)


class CompressionClassModel(models.Model):
    objects = None
    compression_class = models.CharField(max_length=8)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Compression Class'
        verbose_name_plural = 'Compression Class'

    def __str__(self):
        return f'{self.compression_class}'


class SideModel(models.Model):
    objects = None
    side = models.CharField(max_length=8)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Side'
        verbose_name_plural = 'Side'

    def __str__(self):
        return f'{self.side}'


class ProductCategoryModel(models.Model):
    objects = None
    category = models.CharField(max_length=50)
    category_title = models.CharField(max_length=50)
    short_description = models.TextField()
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.FileField(upload_to=get_category_upload_path)
    image_alt = models.CharField(max_length=256, blank=True, null=True)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    # Date Time Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Category'

    def save(self, *args, **kwargs):
        if self.slug is None:
            original_slug = slugify(self.category)
            unique_slug = original_slug

            num = 1
            while ProductCategoryModel.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1

            self.slug = unique_slug

        # تنظیم priority به ترتیب و بدون فاصله
        if self.priority is None:
            # پیدا کردن آخرین مقدار priority
            last_priority = ProductCategoryModel.objects.count()
            self.priority = last_priority + 1

        super(ProductCategoryModel, self).save(*args, **kwargs)

        # به‌روز رسانی priority برای از بین بردن فاصله‌ها
        all_products = ProductCategoryModel.objects.all().order_by('priority')
        for index, product in enumerate(all_products, start=1):
            if product.priority != index:
                product.priority = index
                product.save(update_fields=['priority'])

    def __str__(self) -> str:
        return str(self.category)

    def get_absolute_url(self):
        return f'/category/{self.slug}'


class ProductSubCategoryModel(models.Model):
    objects = None
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50, blank=True, null=True)
    subcategory_title = models.CharField(max_length=50)
    short_description = models.TextField()
    description = models.TextField()
    image = models.FileField(upload_to=get_subcategory_upload_path)
    image_alt = models.CharField(max_length=256, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    # Date Time Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product SubCategory'
        verbose_name_plural = 'Product SubCategory'

    def save(self, *args, **kwargs):
        if self.slug is None:
            original_slug = slugify(self.subcategory)
            unique_slug = original_slug

            num = 1
            while ProductSubCategoryModel.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1

            self.slug = unique_slug

        # تنظیم priority به ترتیب و بدون فاصله
        if self.priority is None:
            # پیدا کردن آخرین مقدار priority
            last_priority = ProductSubCategoryModel.objects.count()
            self.priority = last_priority + 1

        super(ProductSubCategoryModel, self).save(*args, **kwargs)

        # به‌روز رسانی priority برای از بین بردن فاصله‌ها
        all_products = ProductSubCategoryModel.objects.all().order_by('priority')
        for index, product in enumerate(all_products, start=1):
            if product.priority != index:
                product.priority = index
                product.save(update_fields=['priority'])

    def __str__(self):
        return f'{self.slug}'

    def get_absolute_url(self):
        return f'/category/{self.category}/{self.slug}'


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
    image_alt = models.CharField(max_length=256, blank=True, null=True)

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


@receiver(pre_save, sender=ProductCategoryModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.priority is None:
        instance.priority = 1

    if instance.pk:
        existing_instance = ProductCategoryModel.objects.get(pk=instance.pk)
        current_priority = existing_instance.priority or 0
        update_priority = instance.priority or 0

        if current_priority > update_priority:
            ProductCategoryModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                priority=models.F('priority') + 1)
        elif current_priority < update_priority:
            ProductCategoryModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                priority=models.F('priority') - 1)

    elif not instance.pk:
        last_number = ProductCategoryModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if not instance.priority:
            instance.priority = (last_number or 0) + 1
        else:
            if ProductCategoryModel.objects.filter(priority__lte=instance.priority).exists():
                ProductCategoryModel.objects.filter(priority__gte=instance.priority).update(
                    priority=models.F('priority') + 1)


@receiver(pre_save, sender=ProductSubCategoryModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.priority is None:
        instance.priority = 1

    if instance.pk:
        existing_instance = ProductSubCategoryModel.objects.get(pk=instance.pk)
        current_priority = existing_instance.priority or 0
        update_priority = instance.priority or 0

        if current_priority > update_priority:
            ProductSubCategoryModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                priority=models.F('priority') + 1)
        elif current_priority < update_priority:
            ProductSubCategoryModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                priority=models.F('priority') - 1)

    elif not instance.pk:
        last_number = ProductSubCategoryModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if not instance.priority:
            instance.priority = (last_number or 0) + 1
        else:
            if ProductSubCategoryModel.objects.filter(priority__lte=instance.priority).exists():
                ProductSubCategoryModel.objects.filter(priority__gte=instance.priority).update(
                    priority=models.F('priority') + 1)


@receiver(pre_save, sender=SideModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.pk:
        existing_instance = SideModel.objects.get(pk=instance.pk)
        if not existing_instance.priority:
            last_number = SideModel.objects.aggregate(max_number=Max('priority'))['max_number']
            existing_instance.priority = last_number
        else:
            current_priority = existing_instance.priority
            update_priority = instance.priority
            if current_priority > update_priority:
                SideModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                    priority=models.F('priority') + 1)
            if current_priority < update_priority:
                SideModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                    priority=models.F('priority') - 1)

    elif not instance.pk and not instance.priority:
        last_number = SideModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if last_number:
            instance.priority = last_number + 1
        else:
            instance.priority = 1

    elif not instance.pk and instance.priority:
        if SideModel.objects.filter(priority__lte=instance.priority).exists():
            SideModel.objects.filter(priority__gte=instance.priority).update(
                priority=models.F('priority') + 1)


@receiver(pre_save, sender=CompressionClassModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.pk:
        existing_instance = CompressionClassModel.objects.get(pk=instance.pk)
        if not existing_instance.priority:
            last_number = CompressionClassModel.objects.aggregate(max_number=Max('priority'))['max_number']
            existing_instance.priority = last_number
        else:
            current_priority = existing_instance.priority
            update_priority = instance.priority
            if current_priority > update_priority:
                CompressionClassModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                    priority=models.F('priority') + 1)
            if current_priority < update_priority:
                CompressionClassModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                    priority=models.F('priority') - 1)

    elif not instance.pk and not instance.priority:
        last_number = CompressionClassModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if last_number:
            instance.priority = last_number + 1
        else:
            instance.priority = 1

    elif not instance.pk and instance.priority:
        if CompressionClassModel.objects.filter(priority__lte=instance.priority).exists():
            CompressionClassModel.objects.filter(priority__gte=instance.priority).update(
                priority=models.F('priority') + 1)


class AddImageGalleryModel(models.Model):
    objects = None
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='image_gallery_product')
    color = models.ForeignKey('ColorProductModel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_gallery_upload_path, blank=True, null=True)
    image_alt = models.CharField(max_length=256, blank=True, null=True)

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
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    fav = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
        ]


class Site(models.Model):
    domain = models.CharField(max_length=256)
    name = models.CharField(max_length=256)


class CouponModel(models.Model):
    objects = None
    customer = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_percent = models.CharField(max_length=20, default=0, blank=True, null=True)
    discount_amount = models.CharField(max_length=20, default=0, blank=True, null=True)
    discount_threshold = models.CharField(max_length=20, default=0, blank=True, null=True)
    all_product = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    infinite = models.BooleanField(default=False)
    limit = models.IntegerField(default=1, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField()
    extra_discount = models.BooleanField(default=False)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.created <= now <= self.expire

    def __str__(self):
        return f'{self.customer} - {self.coupon_code}'


class ProductCouponModel(models.Model):
    coupon = models.ForeignKey(CouponModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)


class CustomerTypeModel(models.Model):
    customer_type = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.customer_type}'


class ProductTypeModel(models.Model):
    product_type = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product_type}'


class BodyAreaModel(models.Model):
    body_area = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.body_area}'


class ClassNumberModel(models.Model):
    class_num = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.class_num}'


class TreatmentCategoryModel(models.Model):
    treatment_category = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.treatment_category}'


class HearAboutUsModel(models.Model):
    hear_about_us = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.hear_about_us}'


class CustomMadeModel(models.Model):
    customer_type = models.ForeignKey(CustomerTypeModel, on_delete=models.CASCADE)
    other_customer_type = models.CharField(max_length=64, blank=True, null=True)
    clinic_name = models.CharField(max_length=32, blank=True, null=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32)
    phone_prefix = models.CharField(max_length=8)
    product_type = models.ForeignKey(ProductTypeModel, on_delete=models.CASCADE)
    body_area = models.ForeignKey(BodyAreaModel, on_delete=models.CASCADE)
    class_num = models.ForeignKey(ClassNumberModel, on_delete=models.CASCADE)
    treatment_category = models.ForeignKey(TreatmentCategoryModel, on_delete=models.CASCADE)
    description = models.TextField()
    hear_about_us = models.ForeignKey(HearAboutUsModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'


class CustomMadeAttachFileModel(models.Model):
    custom_made = models.ForeignKey(CustomMadeModel, on_delete=models.CASCADE)
    attach_file = models.FileField(upload_to=get_attach_file_upload_path, null=True, blank=True)

    def __str__(self):
        return f'{self.custom_made}'


class CustomMadePageModel(models.Model):
    image_desktop = models.ImageField(upload_to=get_custom_made_upload_path)
    image_mobile = models.ImageField(upload_to=get_custom_made_upload_path)
    image_alt = models.CharField(max_length=256, blank=True, null=True)

    content1_text = models.TextField()
    content1_right_title = models.CharField(max_length=32)
    content1_right_image = models.ImageField(upload_to=get_custom_made_upload_path)
    content1_right_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content1_mid_title = models.CharField(max_length=326)
    content1_mid_image = models.ImageField(upload_to=get_custom_made_upload_path)
    content1_mid_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content1_left_title = models.CharField(max_length=32)
    content1_left_image = models.ImageField(upload_to=get_custom_made_upload_path)
    content1_left_image_alt = models.CharField(max_length=256, blank=True, null=True)

    content2_text = models.TextField()
    content2_image = models.ImageField(upload_to=get_custom_made_upload_path)
    content2_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content2_link = models.CharField(max_length=128)

    content3_text = models.TextField()
    content3_right = models.TextField()
    content3_mid = models.TextField()
    content3_left = models.TextField()

    content4_text = models.TextField()
    content4_image = models.ImageField(upload_to=get_custom_made_upload_path)
    content4_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content4_right = models.TextField()
    content4_mid = models.TextField()
    content4_left = models.TextField()
    content4_link_explore = models.CharField(max_length=128)
    content4_link_place_order = models.CharField(max_length=128)

    customer_testimonials = models.TextField()

    def __str__(self):
        return f'CustomMadePage'


class CustomerTestimonialsModel(models.Model):
    name = models.CharField(max_length=32)
    testimonial = models.TextField

    def __str__(self):
        return f'{self.name}'


# class BrandPageModel(models.Model):
#     brand = models.ForeignKey(ProductBrandModel, on_delete=models.CASCADE)
#     image_desktop = models.ImageField(upload_to=get_brand_upload_path)
#     image_mobile = models.ImageField(upload_to=get_brand_upload_path)
#     image_alt = models.CharField(max_length=64, blank=True, null=True)
#
#     content1_title = models.CharField(max_length=64)
#     content1_image = models.ImageField(upload_to=get_brand_upload_path)
#     content1_image_alt = models.CharField(max_length=64, blank=True, null=True)
#     content1_text = models.TextField()
#
#     content2_text = models.TextField()
#     content2_right_image = models.ImageField(upload_to=get_brand_upload_path)
#     content2_right_image_alt = models.CharField(max_length=64, blank=True, null=True)
#     content2_right = models.TextField()
#     content2_mid_image = models.ImageField(upload_to=get_brand_upload_path)
#     content2_mid_image_alt = models.CharField(max_length=64, blank=True, null=True)
#     content2_mid = models.TextField()
#     content2_left_image = models.ImageField(upload_to=get_brand_upload_path)
#     content2_left_image_alt = models.CharField(max_length=64, blank=True, null=True)
#     content2_left = models.TextField()
#
#     contact_image = models.ImageField(upload_to=get_brand_upload_path)
#     contact_image_alt = models.CharField(max_length=64, blank=True, null=True)
#     contact_text = models.TextField()
#
#     def __str__(self):
#         return f'{self.brand}'


class ProductBrandModel(models.Model):
    brand = models.CharField(max_length=32)
    brand_logo = models.ImageField(upload_to=get_brand_logo_upload_path, null=True, blank=True)
    brand_logo_alt = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(unique=True)

    image_desktop = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    image_mobile = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    image_alt = models.CharField(max_length=256, blank=True, null=True)

    content1_title = models.CharField(max_length=64, blank=True, null=True)
    content1_image = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    content1_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content1_text = models.TextField(blank=True, null=True)

    content2_text = models.TextField(blank=True, null=True)
    content2_right_image = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    content2_right_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content2_right = models.TextField(blank=True, null=True)
    content2_mid_image = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    content2_mid_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content2_mid = models.TextField(blank=True, null=True)
    content2_left_image = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    content2_left_image_alt = models.CharField(max_length=256, blank=True, null=True)
    content2_left = models.TextField(blank=True, null=True)

    contact_image = models.ImageField(upload_to=get_brand_upload_path, blank=True, null=True)
    contact_image_alt = models.CharField(max_length=256, blank=True, null=True)
    contact_text = models.TextField(blank=True, null=True)

    active_page = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.brand}'


class BrandCartModel(models.Model):
    brand = models.ForeignKey(ProductBrandModel, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.brand}'


class BrandCartImageModel(models.Model):
    brand_cart = models.ForeignKey(BrandCartModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_brand_cart_upload_path)
    image_alt = models.CharField(max_length=256, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f'{self.brand_cart.brand} - Image {self.priority}'
