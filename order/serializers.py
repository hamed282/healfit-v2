from rest_framework import serializers
from .models import OrderModel, OrderItemModel


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemModel
        fields = ['product', 'price', 'quantity', 'image']

    def get_image(self, obj):
        product = obj.product.product
        image = product.cover_image
        if image == '':
            image = 'None'
        else:
            image = image.url
        return image


class OrderUserSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='status', read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['status', 'transaction_ref', 'created', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.price for item in obj.items.all())
