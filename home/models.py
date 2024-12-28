from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models import Max


class BannerSliderModel(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='settings/banner-slide/', verbose_name='image (1455*505 px)')
    banner_alt = models.CharField(max_length=125)
    link = models.CharField(max_length=512, null=True, blank=True)
    priority = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Banner Slider'
        verbose_name_plural = 'Banner Sliders'

    def save(self, *args, **kwargs):
        if self.priority is None:
            last_priority = BannerSliderModel.objects.count()
            self.priority = last_priority + 1

        super(BannerSliderModel, self).save(*args, **kwargs)

        all_image = BannerSliderModel.objects.all().order_by('priority')
        for index, image in enumerate(all_image, start=1):
            if image.priority != index:
                image.priority = index
                image.save(update_fields=['priority'])

    def __str__(self):
        return f'{self.title}'


@receiver(pre_save, sender=BannerSliderModel)
def increment_numbers_after_existing(sender, instance, **kwargs):
    if instance.priority is None:
        instance.priority = 1

    if instance.pk:
        existing_instance = BannerSliderModel.objects.get(pk=instance.pk)
        current_priority = existing_instance.priority or 0
        update_priority = instance.priority or 0

        if current_priority > update_priority:
            BannerSliderModel.objects.filter(priority__lt=current_priority, priority__gte=update_priority).update(
                priority=models.F('priority') + 1)
        elif current_priority < update_priority:
            BannerSliderModel.objects.filter(priority__gt=current_priority, priority__lte=update_priority).update(
                priority=models.F('priority') - 1)

    elif not instance.pk:
        last_number = BannerSliderModel.objects.aggregate(max_number=Max('priority'))['max_number']
        if not instance.priority:
            instance.priority = (last_number or 0) + 1
        else:
            if BannerSliderModel.objects.filter(priority__lte=instance.priority).exists():
                BannerSliderModel.objects.filter(priority__gte=instance.priority).update(
                    priority=models.F('priority') + 1)


class VideoHomeModel(models.Model):
    objects = None
    video = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'video'

    def __str__(self):
        return f'Video'

    def clean(self):
        if not self.pk and VideoHomeModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Video you can not add another"
            )


class CommentHomeModel(models.Model):
    objects = None
    name = models.CharField(max_length=32)
    comment = models.TextField()
    active = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class ContentHomeModel(models.Model):
    objects = None
    content = models.TextField()

    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Content'

    def __str__(self):
        return f'Content'

    def clean(self):
        if not self.pk and ContentHomeModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Video you can not add another"
            )


class SEOHomeModel(models.Model):
    objects = None
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'SEO Fields'

    def clean(self):
        if not self.pk and SEOHomeModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one SEO Fields you can not add another"
            )


class LogoModel(models.Model):
    objects = None
    logo = models.FileField(upload_to='settings/logo/')
    logo_alt = models.CharField(max_length=125)
    fav = models.FileField(upload_to='settings/fav/')

    def __str__(self):
        return f'Logo and Fav Icon'

    def clean(self):
        if not self.pk and LogoModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Logo you can not add another"
            )


class BannerShopModel(models.Model):
    objects = None
    image = models.ImageField(upload_to='banner_shop/images/')
    link = models.CharField(max_length=512, null=True, blank=True)

    def clean(self):
        if BannerShopModel.objects.count() >= 3 and not self.pk:
            raise ValidationError('Only 3 banners are allowed.')

    def save(self, *args, **kwargs):
        self.clean()
        super(BannerShopModel, self).save(*args, **kwargs)


class NewsLetterModel(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'NewsLetter'
        verbose_name_plural = 'NewsLetter'


class ContactSubmitModel(models.Model):
    objects = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Contact User Submit'
        verbose_name_plural = 'Contact User Submit'


class TelegramBotModel(models.Model):
    objects = None
    username = models.CharField(max_length=64)
    chat_id = models.CharField(max_length=64)

    def __str__(self):
        return self.chat_id


class AboutPageModel(models.Model):
    objects = None
    body = models.TextField()
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'About Page'

    def clean(self):
        if not self.pk and AboutPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one About Page you can not add another"
            )


class ContactUsPageModel(models.Model):
    objects = None
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'ContactUs Page'

    def clean(self):
        if not self.pk and ContactUsPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one ContactUs Page you can not add another"
            )


class CustomerCarePageModel(models.Model):
    objects = None
    body = models.TextField()
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'CustomerCare Page'

    def clean(self):
        if not self.pk and CustomerCarePageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one CustomerCare Page you can not add another"
            )


class WholesaleInquiryPageModel(models.Model):
    objects = None
    body = models.TextField()
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'WholesaleInquiry Page'

    def clean(self):
        if not self.pk and WholesaleInquiryPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one WholesaleInquiry Page you can not add another"
            )


class RefundPolicyPageModel(models.Model):
    objects = None
    body = models.TextField()
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'RefundPolicy Page'

    def clean(self):
        if not self.pk and RefundPolicyPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one RefundPolicy Page you can not add another"
            )


class SitemapPageModel(models.Model):
    objects = None
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Sitemap Page'

    def clean(self):
        if not self.pk and SitemapPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Sitemap Page you can not add another"
            )


class CareerPageModel(models.Model):
    objects = None
    body = models.TextField()
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Career Page'

    def clean(self):
        if not self.pk and CareerPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Career Page you can not add another"
            )


class ShopPageModel(models.Model):
    objects = None
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Shop Page'

    def clean(self):
        if not self.pk and ShopPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Shop Page you can not add another"
            )


class BlogPageModel(models.Model):
    objects = None
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    schema_markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Blog Page'

    def clean(self):
        if not self.pk and BlogPageModel.objects.exists():
            # This below line will render error by breaking page, you will see
            raise ValidationError(
                "There can be only one Blog Page you can not add another"
            )
