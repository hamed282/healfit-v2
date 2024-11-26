from rest_framework import serializers
from .models import (BannerSliderModel, VideoHomeModel, CommentHomeModel, ContentHomeModel, BannerShopModel,
                     SEOHomeModel, LogoModel, NewsLetterModel, ContactSubmitModel, AboutPageModel, ShopPageModel,
                     CareerPageModel, RefundPolicyPageModel, SitemapPageModel, ContactUsPageModel, BlogPageModel,
                     CustomerCarePageModel, WholesaleInquiryPageModel)


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


class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterModel
        fields = '__all__'


class ContactSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmitModel
        fields = '__all__'


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPageModel
        fields = '__all__'


class ContactUsPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsPageModel
        fields = '__all__'


class CustomerCarePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCarePageModel
        fields = '__all__'


class WholesaleInquiryPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholesaleInquiryPageModel
        fields = '__all__'


class RefundPolicyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundPolicyPageModel
        fields = '__all__'


class SitemapPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitemapPageModel
        fields = '__all__'


class CareerPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPageModel
        fields = '__all__'


class ShopPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPageModel
        fields = '__all__'


class BlogPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPageModel
        fields = '__all__'
