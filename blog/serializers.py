from rest_framework import serializers
from .models import BlogModel


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = '__all__'


class BlogAllSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']
