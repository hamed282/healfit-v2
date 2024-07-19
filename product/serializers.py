from rest_framework import serializers
from .models import ProductGenderModel


class ProductGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGenderModel
        fields = '__all__'
