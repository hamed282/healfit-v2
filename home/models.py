from django.db import models
from django.core.exceptions import ValidationError


class BannerSliderModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='images/home/', verbose_name='image (1455*505 px)')
    active = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Banner Slider'
        verbose_name_plural = 'Banner Sliders'

    def __str__(self):
        return f'{self.title}'


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
    name = models.CharField(max_length=32)
    comment = models.TextField()
    active = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

