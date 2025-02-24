from django.contrib import admin
from .models import (BlogModel, BlogTagModel, AddBlogTagModel, BlogCategoryModel, BlogImageModel, CommentBlogModel,
                     AddCategoryModel)


class TagInline(admin.TabularInline):
    model = AddCategoryModel
    extra = 1


class CategoryInline(admin.TabularInline):
    model = AddBlogTagModel
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    # list_display = ['id', 'blog']
    inlines = (TagInline, CategoryInline)


class BlogTagAdmin(admin.ModelAdmin):
    # readonly_fields = ["slug"]
    list_display = ['tag']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created', 'is_reply']
    raw_id_fields = ['user', 'blog', 'reply']


admin.site.register(BlogModel, BlogAdmin)
admin.site.register(BlogTagModel, BlogTagAdmin)
admin.site.register(BlogCategoryModel)
admin.site.register(AddBlogTagModel)
admin.site.register(BlogImageModel)
admin.site.register(CommentBlogModel, CommentAdmin)
