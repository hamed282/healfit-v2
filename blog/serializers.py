from rest_framework.serializers import ModelSerializer, DateField, SerializerMethodField, SlugRelatedField
from .models import BlogModel, AddBlogTagModel, BlogCategoryModel


class BlogSerializer(ModelSerializer):
    meta_tag = SerializerMethodField()
    category = SlugRelatedField(slug_field='category', read_only=True)

    class Meta:
        model = BlogModel
        fields = '__all__'

    def get_meta_tag(self, obj):
        try:
            tag = AddBlogTagModel.objects.get(blog=obj)
            tag = tag.tag.tag
        except:
            tag = None

        return tag


class BlogAllSerializer(ModelSerializer):
    created = DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class RelatedBlogSerializer(ModelSerializer):
    created = DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class MetaCategorySerializer(ModelSerializer):
    class Meta:
        model = BlogCategoryModel
        fields = '__all__'
