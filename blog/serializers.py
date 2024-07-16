from rest_framework.serializers import ModelSerializer, DateField, SerializerMethodField
from .models import BlogModel, AddBlogTagModel


class BlogSerializer(ModelSerializer):
    meta_tag = SerializerMethodField()

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



