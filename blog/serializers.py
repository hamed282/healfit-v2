from rest_framework.serializers import ModelSerializer, DateField
from .models import BlogModel, BlogTagModel


class BlogSerializer(ModelSerializer):
    class Meta:
        model = BlogModel
        fields = '__all__'


class BlogAllSerializer(ModelSerializer):
    created = DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class BlogTagSerializer(ModelSerializer):
    class Meta:
        model = BlogTagModel
        fields = '__all__'
