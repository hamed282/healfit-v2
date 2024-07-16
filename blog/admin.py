from django.contrib import admin
from .models import BlogModel, BlogTagModel, AddBlogTagModel


class TagInline(admin.TabularInline):
    model = AddBlogTagModel
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    # list_display = ['id', 'blog']
    inlines = (TagInline, )


class BlogTagAdmin(admin.ModelAdmin):
    # readonly_fields = ["slug"]
    list_display = ['tag']


admin.site.register(BlogModel, BlogAdmin)
admin.site.register(BlogTagModel, BlogTagAdmin)
