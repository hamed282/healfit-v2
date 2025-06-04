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
        amount_aed = self.order.get_total_price()
        
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
                    "phone": self.order.address.phone_number,
                    "email": self.order.user.email,
                    "name": f"{self.order.user.first_name} {self.order.user.last_name}",
                    # dob is optional, add if available
                },
                "shipping_address": {
                    "city": self.order.address.city if hasattr(self.order.address, 'city') else "",
                    "address": self.order.address.address if hasattr(self.order.address, 'address') else "",
                    "zip": "1111"  # Placeholder, update if you have zip
                },
                "order": {
                    "tax_amount": "0.00",
                    "shipping_amount": "0.00",
                    "discount_amount": "0.00",
                    "updated_at": timezone.now().isoformat(),
                    "reference_id": str(self.order.id),
                    "items": [
                        {
                            "title": "item.product.name",
                            "description": "item.product.name",  # Placeholder, update if you have description
                            "quantity": 1,
                            "unit_price": "1000",
                            "discount_amount": "0.00",
                            "reference_id": "SKU123",
                            "image_url": "https://example.com/",  # Placeholder
                            "product_url": "https://example.com/",  # Placeholder
                            "gender": "Other",  # Placeholder, update if you have gender
                            "category": "Clothes",  # Placeholder, update if you have category
                            "color": "white",  # Placeholder, update if you have color
                            "product_material": "cotton",  # Placeholder, update if you have material
                            "size_type": "EU",  # Placeholder, update if you have size_type
                            "size": "M",  # Placeholder, update if you have size
                            "brand": "Brand",  # Placeholder, update if you have brand
                            "is_refundable": True
                        }
                    ]
                },
                # Optional fields below, add if you have data
                # "buyer_history": {...},
                # "order_history": [...],
                # "meta": {...},
                # "attachment": {...},
            },
            "lang": "en",
            "merchant_code": self.config['MERCHANT_CODE'],
            "merchant_urls": {
                "success": self.config['SUCCESS_URL'],
                "cancel": self.config['CANCEL_URL'],
                "failure": self.config['FAILURE_URL'],
            },
            # "token": None,  # Optional
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