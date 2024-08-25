from django.db import models
from upload_path import get_cover_blog_upload_path, get_title_blog_upload_path, get_banner_blog_upload_path


class BlogCategoryModel(models.Model):
    category = models.CharField(max_length=16, unique=True)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, null=True, blank=True)
    meta_description = models.CharField(max_length=160, null=True, blank=True)

    def __str__(self):
        return f'{self.category}'


class BlogTagModel(models.Model):
    objects = None
    tag = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blogs Tag'

    def __str__(self):
        return f'{self.tag}'


class BlogModel(models.Model):
    cover_image = models.ImageField(upload_to=get_cover_blog_upload_path)
    cover_image_alt = models.CharField(max_length=32)
    banner = models.ImageField(upload_to=get_banner_blog_upload_path)
    banner_alt = models.CharField(max_length=32)
    title = models.CharField(max_length=250)
    title_image = models.ImageField(upload_to=get_title_blog_upload_path)
    title_image_alt = models.CharField(max_length=32)
    short_description = models.TextField(max_length=60)
    description = models.TextField()
    body = models.TextField()
    author = models.CharField(max_length=64)
    role = models.CharField(max_length=24)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategoryModel, on_delete=models.CASCADE)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, null=True, blank=True)
    meta_description = models.CharField(max_length=160, null=True, blank=True)
    schema_markup = models.TextField(null=True, blank=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class AddBlogTagModel(models.Model):
    objects = None
    tag = models.OneToOneField(BlogTagModel, on_delete=models.CASCADE, unique=True)
    blog = models.OneToOneField(BlogModel, on_delete=models.CASCADE, related_name='blog_tag')

    def __str__(self):
        return f'{self.tag}'


class BlogImageModel(models.Model):
    image = models.ImageField(upload_to='blog/blog/')
    type = models.CharField(max_length=32)
