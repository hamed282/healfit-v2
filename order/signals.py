# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import OrderModel, OrderStatusModel
# from services.send_order_message import send_inprocess_email  # فرض کنید تابع ایمیل در این مسیر ذخیره شده است
# from django.db import transaction
#
#
# @receiver(post_save, sender=OrderModel)
# def send_email_on_status_change(sender, instance, **kwargs):
#     # بررسی تغییر وضعیت به inprocess
#     if instance.status.status == 'In process':  # فرض بر این است که فیلد name در مدل وضعیت وجود دارد
#         recipient_list = ['hamed.alizadegan@gmail.com']  # ایمیل کاربر را دریافت می‌کنیم
#         transaction.on_commit(lambda: send_inprocess_email(instance, recipient_list))
