from rest_framework import serializers
from .models import (BannerSliderModel, VideoHomeModel, CommentHomeModel, ContentHomeModel, BannerShopModel,
                     SEOHomeModel, LogoModel)


class BannerSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerSliderModel
        fields = '__all__'


class CommentHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentHomeModel
        fields = '__all__'


class VideoHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoHomeModel
        fields = '__all__'


class ContentHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentHomeModel
        fields = '__all__'


class BannerShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerShopModel
        fields = '__all__'


class LogoHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoModel
        fields = '__all__'


class SEOHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOHomeModel
        fields = '__all__'
