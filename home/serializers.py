from rest_framework import serializers
from .models import BannerSliderModel


class BannerSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerSliderModel
        fields = '__all__'

