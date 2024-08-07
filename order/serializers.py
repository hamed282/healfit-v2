from rest_framework import serializers
from .models import OrderItemModel


class OrderUserSerializer(serializers.ModelSerializer):
    size = serializers.SlugRelatedField(slug_field='size', read_only=True)
    color = serializers.SlugRelatedField(slug_field='color', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemModel
        fields = ['product', 'image', 'price', 'size', 'color', 'quantity', 'trace', 'created']

    def get_image(self, obj):
        product = obj.product.product
        image = product.cover_image
        if image == '':
            image = 'None'
        else:
            image = image.url
        return image
