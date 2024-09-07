from django.contrib import admin
from .models import OrderItemModel, OrderModel, OrderStatusModel


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    raw_id_fields = ('product',)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid', 'status')
    list_filter = ('paid', 'status')
    readonly_fields = ['ref_id', 'cart_id', 'trace', 'error_message', 'error_note', 'transaction_ref']
    inlines = (OrderItemInline,)


admin.site.register(OrderStatusModel)
