from django.contrib import admin
from .models import OrderItemModel, OrderModel, OrderStatusModel, UserProductModel, ShippingModel, ShippingCountryModel


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    raw_id_fields = ('product',)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid', 'status')
    list_filter = ('paid', 'status')
    inlines = (OrderItemInline,)


class ShippingInline(admin.TabularInline):
    model = ShippingModel
    raw_id_fields = ('country',)
    extra = 1


class ShippingCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country')
    list_filter = ('country',)
    inlines = (ShippingInline,)


admin.site.register(OrderStatusModel)
admin.site.register(OrderItemModel)
admin.site.register(UserProductModel)
admin.site.register(ShippingCountryModel, ShippingCountryAdmin)
