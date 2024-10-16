from django.db import models
from accounts.models import User
from product.models import ProductVariantModel, ColorProductModel, SizeProductModel, CouponModel
from accounts.models import AddressModel


class OrderStatusModel(models.Model):
    status = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.status}'


class OrderModel(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, related_name='address_order')
    status = models.ForeignKey(OrderStatusModel, on_delete=models.CASCADE, related_name='status_order')
    ref_id = models.CharField(max_length=200, blank=True, null=True)
    transaction_ref = models.CharField(max_length=200, blank=True, null=True)
    cart_id = models.CharField(max_length=64, blank=True, null=True)
    trace = models.CharField(max_length=200, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    error_note = models.TextField(blank=True, null=True)
    coupon = models.ForeignKey(CouponModel, on_delete=models.CASCADE, blank=True, null=True)
    total_discount = models.CharField(max_length=9, blank=True, null=True)
    total_amount = models.CharField(max_length=9, blank=True, null=True)

    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('paid', '-created')

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.user} - Order ID: {self.id}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItemModel(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order_item')
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductVariantModel, on_delete=models.CASCADE, related_name='order_product')
    color = models.ForeignKey(ColorProductModel, on_delete=models.CASCADE, related_name='order_color')
    size = models.ForeignKey(SizeProductModel, on_delete=models.CASCADE, related_name='order_size')
    price = models.IntegerField()
    discount_price = models.IntegerField()
    selling_price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.selling_price * self.quantity


class UserProductModel(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_user')
    product = models.ForeignKey(ProductVariantModel, on_delete=models.CASCADE, related_name='rel_product')
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='rel_order')
    price = models.CharField(max_length=20)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order}'


class ShippingModel(models.Model):
    country = models.CharField(max_length=24)
    city = models.CharField(max_length=24, blank=True, null=True)
    threshold_free = models.CharField(max_length=9)
    shipping_fee = models.CharField(max_length=9)
