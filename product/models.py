from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Max
import os


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
