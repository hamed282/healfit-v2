import requests
import json
from .tabby_config import TABBY_CONFIG
from django.conf import settings
from order.models import OrderModel
from django.utils import timezone

class TabbyPayment:
    def __init__(self, order_id):
        self.order = OrderModel.objects.get(id=order_id)
        self.config = TABBY_CONFIG
        self.headers = {
            'Authorization': f'Bearer {self.config["API_KEY"]}',
            'Content-Type': 'application/json'
        }

    def create_payment_session(self):
        """ایجاد جلسه پرداخت Tabby"""
        url = f"{self.config['API_URL']}checkout"
        
        # تبدیل مبلغ به درهم
        amount_aed = self.order.total_price / 10  # فرض بر این که قیمت به ریال است و هر درهم 10 ریال
        
        if amount_aed < self.config['MIN_AMOUNT']:
            raise ValueError(f"مبلغ خرید باید حداقل {self.config['MIN_AMOUNT']} درهم باشد")
            
        if amount_aed > self.config['MAX_AMOUNT']:
            raise ValueError(f"مبلغ خرید نباید بیشتر از {self.config['MAX_AMOUNT']} درهم باشد")

        payload = {
            "payment": {
                "amount": str(amount_aed),
                "currency": self.config['CURRENCY'],
                "description": f"خرید از {settings.SITE_NAME}",
                "buyer": {
                    "phone": self.order.phone_number,
                    "email": self.order.email,
                    "name": f"{self.order.first_name} {self.order.last_name}",
                },
                "order": {
                    "reference_id": str(self.order.id),
                    "items": [
                        {
                            "title": item.product.product,
                            "quantity": item.quantity,
                            "unit_price": str(item.price / 10),  # تبدیل به درهم
                        } for item in self.order.order_items.all()
                    ]
                }
            },
            "lang": "ar",
            "merchant_code": self.config['MERCHANT_CODE'],
            "merchant_urls": {
                "success": self.config['SUCCESS_URL'],
                "failure": self.config['FAILURE_URL'],
                "cancel": self.config['CANCEL_URL'],
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"خطا در ایجاد جلسه پرداخت Tabby: {str(e)}")

    def verify_payment(self, payment_id):
        """تأیید پرداخت Tabby"""
        url = f"{self.config['API_URL']}payments/{payment_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            payment_data = response.json()
            
            if payment_data['status'] == 'AUTHORIZED':
                self.order.payment_status = 'PAID'
                self.order.payment_method = 'TABBY'
                self.order.payment_date = timezone.now()
                self.order.save()
                return True
            return False
        except requests.exceptions.RequestException as e:
            raise Exception(f"خطا در تأیید پرداخت Tabby: {str(e)}")

    def cancel_payment(self, payment_id):
        """لغو پرداخت Tabby"""
        url = f"{self.config['API_URL']}payments/{payment_id}/cancel"
        
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"خطا در لغو پرداخت Tabby: {str(e)}") 