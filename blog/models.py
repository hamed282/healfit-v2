from django.db import models


class BlogCategoryModel(models.Model):
    category = models.CharField(max_length=16)

    # SEO Fields
    follow = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    canonical = models.CharField(max_length=256, null=True, blank=True)
    meta_title = models.CharField(max_length=60)
    meta_description = models.CharField(max_length=150)

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
    cover_image = models.ImageField(upload_to='blog/cover/')
    cover_image_alt = models.CharField(max_length=32)
    banner = models.ImageField(upload_to='blog/banner/')
    banner_alt = models.CharField(max_length=32)
    title = models.CharField(max_length=250)
    title_image = models.ImageField(upload_to='blog/title/')
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
    meta_title = models.CharField(max_length=60)
    meta_description = models.CharField(max_length=150)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class AddBlogTagModel(models.Model):
    objects = None
    tag = models.OneToOneField(BlogTagModel, on_delete=models.CASCADE, unique=True)
    blog = models.OneToOneField(BlogModel, on_delete=models.CASCADE, related_name='blog_tag')

    def __str__(self):
        return f'{self.tag}'