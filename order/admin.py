from django.contrib import admin
from .models import OrderItemModel, OrderModel


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    raw_id_fields = ('product',)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'paid', 'sent')
    list_filter = ('paid', 'sent')
    readonly_fields = ['ref_id', 'cart_id', 'trace', 'error_message', 'error_note']
    inlines = (OrderItemInline,)
