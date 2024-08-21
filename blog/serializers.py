from rest_framework import serializers
from .models import BlogModel, AddBlogTagModel, BlogCategoryModel, BlogImageModel


class BlogSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(required=False, allow_blank=True)
    category = serializers.SlugRelatedField(slug_field='category', queryset=BlogCategoryModel.objects.all(),)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_null=True)
    meta_description = serializers.CharField(max_length=150, required=False, allow_null=True)
    schema_markup = serializers.CharField(max_length=150, required=False, allow_null=True)

    class Meta:
        model = BlogModel
        fields = '__all__'

    def get_tag(self, obj):
        try:
            tag = AddBlogTagModel.objects.get(blog=obj)
            tag = tag.tag.id
        except:
            tag = None

        return tag


class BlogAllSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class RelatedBlogSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class MetaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategoryModel
        fields = '__all__'


class ImageBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImageModel
        fields = '__all__'
