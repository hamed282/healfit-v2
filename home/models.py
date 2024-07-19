from django.db import models
from django.core.exceptions import ValidationError


class BannerSliderModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='images/home/', verbose_name='image (1455*505 px)')

    class Meta:
        verbose_name = 'Banner Slider'
        verbose_name_plural = 'Banner Sliders'

    def __str__(self):
        return f'{self.title}'






