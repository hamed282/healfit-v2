from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Max
import os


class ProductModel(models.Model):
    objects = None
    gender = models.ForeignKey('ProductGenderModel', on_delete=models.CASCADE, related_name='gender_product')
    product = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='images/product/cover/', blank=True, null=True)
    size_table_image = models.ImageField(upload_to='images/product/size_table/', blank=True, null=True)
    description_image = models.ImageField(upload_to='images/product/description/', blank=True, null=True)
    price = models.IntegerField()
    percent_discount = models.IntegerField(null=True, blank=True)
    subtitle = models.CharField(max_length=256)
    application_fields = models.TextField()
    descriptions = models.TextField()
    group_id = models.CharField(max_length=100)
    priority = models.IntegerField(blank=True, null=True, default=1)
    slug = models.SlugField(max_length=100, unique=True)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60)
    meta_description = models.CharField(max_length=150)

    # Date Time Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item Groups'
        verbose_name_plural = 'Item Groups'

    def save(self, **kwargs):
        self.slug = slugify(self.product)
        if self.priority is None:
            self.priority = 1
        super(ProductModel, self).save(**kwargs)

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


class ProductVariantModel(models.Model):
    objects = None
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_color_size')
    name = models.CharField(max_length=200)
    item_id = models.CharField(max_length=100, verbose_name='Product ID')
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


class ProductGenderModel(models.Model):
    objects = None
    gender = models.CharField(max_length=50)
    gender_title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    image = models.FileField(upload_to='images/gender/')

    class Meta:
        verbose_name = 'Product Gender'
        verbose_name_plural = 'Product Gender'

    def save(self, **kwargs):
        self.slug = slugify(self.gender)
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
    image = models.ImageField(upload_to='images/product/gallery/', blank=True, null=True)

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



