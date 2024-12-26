from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderModel, OrderStatusModel
from utils import send_inprocess_email


@receiver(post_save, sender=OrderModel)
def send_email_on_status_change(sender, instance, **kwargs):
    # بررسی تغییر وضعیت به inprocess
    if instance.status.status == 'In process':  # فرض بر این است که فیلد name در مدل وضعیت وجود دارد
        recipient_list = ['hamed.alizadegan@gmail.com']  # ایمیل کاربر را دریافت می‌کنیم
        send_inprocess_email(instance, recipient_list)

