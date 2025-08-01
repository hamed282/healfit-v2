from django.db import models
from upload_path import (get_cover_blog_upload_path, get_title_blog_upload_path, get_banner_blog_upload_path,
                         get_author_upload_path)
from accounts.models import User
from django.utils.text import slugify


class BlogCategoryModel(models.Model):
    objects = None
    category = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, null=True, blank=True)
    meta_description = models.CharField(max_length=160, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.category)
            unique_slug = original_slug
            num = 1
            while BlogCategoryModel.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

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
    cover_image = models.ImageField(upload_to=get_cover_blog_upload_path, max_length=500)
    cover_image_alt = models.CharField(max_length=256)
    # banner = models.ImageField(upload_to=get_banner_blog_upload_path, null=True, blank=True)
    # banner_alt = models.CharField(max_length=125, null=True, blank=True)
    title = models.CharField(max_length=250)
    # title_image = models.ImageField(upload_to=get_title_blog_upload_path, null=True, blank=True)
    # title_image_alt = models.CharField(max_length=125, null=True, blank=True)
    short_description = models.TextField(max_length=160)
    # description = models.TextField(null=True, blank=True)
    body = models.TextField()
    # author = models.CharField(max_length=64)
    # author_image = models.ImageField(upload_to=get_author_upload_path, null=True, blank=True)
    author = models.ForeignKey('AuthorBlogModel', on_delete=models.CASCADE, null=True, blank=True)
    read_duration = models.CharField(max_length=16, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    # role = models.CharField(max_length=24, null=True, blank=True)
    slug = models.SlugField(unique=True)
    # category = models.ForeignKey(BlogCategoryModel, on_delete=models.CASCADE)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60, null=True, blank=True)
    meta_description = models.CharField(max_length=160, null=True, blank=True)
    schema_markup = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return f'/blog/{self.slug}'


class AuthorBlogModel(models.Model):
    author = models.CharField(max_length=64)
    author_image = models.ImageField(upload_to=get_author_upload_path, null=True, blank=True)
    author_image_alt = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'{self.author}'


class AddCategoryModel(models.Model):
    objects = None
    category = models.ForeignKey(BlogCategoryModel, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='cat_blog')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.category} - {self.blog}'


class AddBlogTagModel(models.Model):
    objects = None
    tag = models.OneToOneField(BlogTagModel, on_delete=models.CASCADE, unique=True)
    blog = models.OneToOneField(BlogModel, on_delete=models.CASCADE, related_name='blog_tag')

    def __str__(self):
        return f'{self.tag}'


class BlogImageModel(models.Model):
    image = models.ImageField(upload_to='blog/blog/', max_length=500)
    image_alt = models.CharField(max_length=256)
    type = models.CharField(max_length=32)


class CommentBlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomment')
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='blogcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replycomment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=512)
    new_comment = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'
