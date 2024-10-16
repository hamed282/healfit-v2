from django.contrib import admin
from .models import OrderItemModel, OrderModel, OrderStatusModel, UserProductModel, ShippingModel, CountryShippingModel


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    raw_id_fields = ('product',)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid', 'status')
    list_filter = ('paid', 'status')
    inlines = (OrderItemInline,)


admin.site.register(OrderStatusModel)
admin.site.register(OrderItemModel)
admin.site.register(UserProductModel)
admin.site.register(UserProductModel)
admin.site.register(UserProductModel)
