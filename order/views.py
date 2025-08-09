from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests

from product.service import Cart
from services.shipping_utiles import delivery_date
from .models import OrderModel, OrderItemModel, OrderStatusModel, ShippingModel, ShippingCountryModel
from product.models import ProductVariantModel, CouponModel
from order.models import UserProductModel
from accounts.models import AddressModel
from django.shortcuts import get_object_or_404, redirect
from .serializers import OrderUserSerializer
from services.zoho_services import zoho_invoice_quantity_update
from services.send_order_message import (send_order_email, send_order_telegram, send_failed_payment_email,
                                         send_failed_payment_telegram)
from .tabby_payment import TabbyPayment


class OrderPayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        forms = request.data['product']
        discount_code = request.data.get('discount_code', None)

        def shipping_fee(country, city, amount):
            if ShippingCountryModel.objects.filter(country=country).exists():
                country_model = ShippingCountryModel.objects.get(country=country)
                if ShippingModel.objects.filter(country=country_model, city=city).exists():
                    shipping = ShippingModel.objects.get(country=country_model, city=city)
                    if float(shipping.threshold_free) > amount:
                        return shipping.shipping_fee
                    return 0
                else:
                    shipping = ShippingCountryModel.objects.get(country=country)
                    if float(shipping.threshold_free) > amount:
                        return shipping.shipping_fee
                    return 0
            else:
                return 300

        if len(forms) > 0:
            address = get_object_or_404(AddressModel, id=request.data['address_id'])
            order = OrderModel.objects.create(user=request.user, address=address,
                                              status=OrderStatusModel.objects.get(status='New'))

            ################################
            # discount_code = 'ABC'
            discount_percent = None
            discount_amount = None
            if discount_code:
                try:
                    code = CouponModel.objects.get(coupon_code=discount_code)
                    if code.is_valid() and code.active and (code.limit > 0 or code.infinite):

                        if code.discount_percent is not None and int(code.discount_percent) != 0:
                            discount_percent = int(code.discount_percent)

                        elif code.discount_amount is not None and int(code.discount_amount) != 0:
                            discount_amount = int(code.discount_amount)

                except:
                    code = None
            else:
                code = None

            ######################################

            for form in forms:
                # product_group = ProductModel.objects.get(id=form['product_id'])
                # product = ProductVariantModel.objects.get(product=product_group, color=color, size=size)
                product = ProductVariantModel.objects.get(id=form['product_id'])
                color = product.color
                size = product.size

                quantity = form['quantity']

                price = product.price
                discount_price = product.get_off_price()

                selling_price = product.get_off_price()
                if discount_code is not None:
                    try:
                        code = CouponModel.objects.get(coupon_code=discount_code)
                        if code.is_valid() and code.active and (code.limit > 0 or code.infinite):
                            if not code.extra_discount:
                                if discount_percent:
                                    selling_price = price - (price * discount_percent) / 100
                                elif discount_amount:
                                    selling_price = price
                            else:
                                if discount_percent:
                                    selling_price = discount_price - (discount_price * discount_percent) / 100
                                elif discount_amount:
                                    selling_price = discount_price
                    except:
                        code = None
                else:
                    code = None

                OrderItemModel.objects.create(order=order,
                                              user=request.user,
                                              product=product,
                                              price=price,
                                              discount_price=discount_price,
                                              selling_price=selling_price,
                                              quantity=quantity,
                                              color=color,
                                              size=size,)

            def total_price_without_discount():
                total_price = 0
                for frm in forms:
                    prd = ProductVariantModel.objects.get(id=frm['product_id'])
                    qnt = frm['quantity']
                    prc = prd.price
                    total_price += int(qnt) * int(prc)
                return total_price

            def total_price_with_discount():
                total_price = 0
                for frm in forms:
                    prd = ProductVariantModel.objects.get(id=frm['product_id'])
                    qnt = frm['quantity']
                    prc = prd.get_off_price()
                    total_price += int(qnt) * int(prc)
                return total_price

            total_price_without_discount = total_price_without_discount()
            total_price_with_discount = total_price_with_discount()

            if code and not code.extra_discount and int(code.discount_threshold) <= total_price_without_discount:
                if discount_percent:
                    amount = int(
                        total_price_without_discount - (total_price_without_discount * int(discount_percent)) / 100)
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
                elif discount_amount:
                    amount = int(total_price_without_discount - int(discount_amount))
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
            elif code and code.extra_discount and int(code.discount_threshold) <= total_price_with_discount:
                if discount_percent:
                    amount = int(total_price_with_discount - (total_price_with_discount * int(discount_percent)) / 100)
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
                elif discount_amount:
                    amount = int(total_price_with_discount - int(discount_amount))
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
            else:
                amount = int(str(order.get_total_price()))
                amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))

            description = f'buy'
            cart_id = str(order.id)
            payload = {
                "method": "create",
                "store": settings.SOTRE_ID,
                "authkey": settings.AUTHKEY,
                "framed": settings.FRAMED,
                "order": {
                    "cartid": cart_id,
                    "test": settings.TEST,
                    "amount": amount_shipping,
                    "currency": settings.CURRENCY,
                    "description": description,
                },
                "return": {
                    "authorised": settings.AUTHORIZED_URL,
                    "declined": settings.DECLINED_URL,
                    "cancelled": settings.CANCELLED_URL,
                },
                "customer": {
                    "email": f"{request.user.email}",
                    "phone": f"{address.phone_number}",

                    "address": {
                        "line1": f"{address.address}",
                        "city": f"{address.city}",
                        "country": f"AE",
                    },
                },
            }

            headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
            response = requests.post(settings.TELR_API_REQUEST, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()

                if 'order' in response:
                    url = response['order']['url']
                    order.ref_id = response['order']['ref']
                    order.cart_id = cart_id
                    order.coupon = code
                    order.total_discount = int(total_price_without_discount) - int(amount)
                    order.total_amount = amount
                    order.shipping = int(shipping_fee(address.country, address.city, amount))
                    order.save()

                    if code and not code.infinite:
                        code.limit -= 1
                        code.save()
                    return Response({'redirect to : ': url}, status=200)
                else:
                    return Response({'Error code: ': str(response['error'])}, status=400)
            else:
                return Response({'details': str(response.json()['errors'])})


def process_order_payment(order):
    """
    عملیات نهایی‌سازی سفارش پس از پرداخت موفق:
    - کاهش موجودی محصولات
    - ثبت UserProductModel
    - ارسال ایمیل و تلگرام
    - بروزرسانی فاکتور زوهو
    """
    if order.paid:
        return False  # قبلاً انجام شده
    order.paid = True
    order.save()
    order_items = order.items.all()
    user = order.user
    for item in order_items:
        product_variant = item.product
        price = product_variant.get_off_price()
        quantity = item.quantity
        product_variant.quantity = product_variant.quantity - quantity
        product_variant.save()
        item.trace = order.trace
        item.save()
        UserProductModel.objects.create(user=user, product=product_variant, order=order,
                                        quantity=quantity, price=price)
    # بروزرسانی فاکتور زوهو
    line_items = [{'item_id': item.product.item_id, 'quantity': item.quantity, "discount_amount": (item.quantity * (item.price - item.discount_price)), "tax_name": "VAT", "tax_type": "tax"} for item in order_items]
    zoho_invoice_quantity_update(order.user.first_name, order.user.last_name, order.user.email,
                                 order.address.address, order.address.city, line_items,
                                 country='United Arab Emirates', customer_id=order.user.zoho_customer_id)
    recipient_list = ['hamed.alizadegan@gmail.com', 'hamed@healfit.ae', order.user.email]
    send_order_email(order, order_items, recipient_list)
    send_order_telegram(order, order_items)
    return True


class OrderPayAuthorisedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            order = OrderModel.objects.filter(user=user).first()
            order.error_note = 'Error 00'
            order.save()
        except Exception as e:
            print('order error')
            print(f'Error occurred: {e}')
            return Response(data={'message': 'invalid order'})
        order.error_note = 'Error 01'
        order.save()
        payload = {
            "method": "check",
            "store": settings.SOTRE_ID,
            "authkey": settings.AUTHKEY,
            "order": {"ref": order.ref_id}
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(settings.TELR_API_VERIFY, json=payload, headers=headers)
        response = response.json()
        order.error_note = 'Error 02'
        order.save()
        if 'order' in response:
            if 'transaction' in response['order']:
                transaction = response['order']['transaction']['ref']
            else:
                transaction = None
            order.trace = response['trace']
            order.transaction_ref = transaction
            order.error_message = '03'
            order.error_note = '03'
            # جلوگیری از عملیات تکراری
            if order.paid:
                return Response(data={'message': 'Order already paid', 'cart_id': order.cart_id, 'transaction_ref': transaction})
            order.save()
            # عملیات پرداخت و ارسال ایمیل فقط یک بار
            process_order_payment(order)

            cart = Cart(request)
            cart.clear()

            return Response(data={'message': 'success', 'cart_id': order.cart_id,
                                  'transaction_ref': transaction})
        else:
            order.paid = False
            order.trace = 'Error 07'
            order.error_message = 'Error 07'
            order.error_note = 'Error 07'
            order.save()

            recipient_list = ['hamed.alizadegan@gmail.com', 'hamed@healfit.ae']
            send_failed_payment_email(recipient_list, 'Failled')
            send_failed_payment_telegram('Failled')

            return Response(data={'message': 'failed'})


class OrderPayDeclinedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # from accounts.models import User
        # user = User.objects.get(id=1)

        try:
            order = OrderModel.objects.filter(user=user).first()
        except:
            return Response(data={'message': 'invalid order'})
        payload = {
            "method": "check",
            "store": settings.SOTRE_ID,
            "authkey": settings.AUTHKEY,
            "order": {"ref": order.ref_id}
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(settings.TELR_API_VERIFY, json=payload, headers=headers)
        response = response.json()

        if 'transaction' in response['order']:
            transaction = response['order']['transaction']['ref']
        else:
            transaction = "Declined"

        order.paid = False
        order.trace = response['trace']
        order.transaction_ref = transaction
        order.error_message = 'Declined'
        order.save()

        recipient_list = ['hamed.alizadegan@gmail.com', 'hamed@healfit.ae']
        send_failed_payment_email(recipient_list, 'Declined')
        send_failed_payment_telegram('Declined')

        return Response(data={'message': 'Declined'})


class OrderPayCancelledView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            order = OrderModel.objects.filter(user=user).first()
        except:
            return Response(data={'message': 'invalid order'})
        payload = {
            "method": "check",
            "store": settings.SOTRE_ID,
            "authkey": settings.AUTHKEY,
            "order": {"ref": order.ref_id}
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(settings.TELR_API_VERIFY, json=payload, headers=headers)
        response = response.json()
        if 'status' in response['order']:
            transaction = response['order']['status']['text']
        else:
            transaction = None

        order.paid = False
        order.trace = response['trace']
        order.transaction_ref = transaction
        order.error_message = 'cancelled'
        order.save()

        recipient_list = ['hamed.alizadegan@gmail.com', 'hamed@healfit.ae']
        send_failed_payment_email(recipient_list, 'Cancelled')
        send_failed_payment_telegram('Cancelled')

        return Response(data={'message': 'Cancelled'})


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_history = OrderModel.objects.filter(user=request.user, paid=True)
        ser_order_history = OrderUserSerializer(instance=order_history, many=True)
        return Response(data=ser_order_history.data)


class ShippingView(APIView):
    def post(self, request):
        country = request.data['country']
        city = request.data['city']
        amount = float(request.data['amount'])
        amount_total = float(request.data['amount_total'])

        if ShippingCountryModel.objects.filter(country=country).exists():
            country_model = ShippingCountryModel.objects.get(country=country)
            if ShippingModel.objects.filter(country=country_model, city=city).exists():
                shipping = ShippingModel.objects.get(country=country_model, city=city)
                if float(shipping.threshold_free) > amount:
                    return Response(data={'shipping_fee': shipping.shipping_fee,
                                          'delivery_time': delivery_date(int(shipping.delivery_day), city),
                                          'total_amount': int(amount),
                                          'subtotal': round(int(amount)/1.05),
                                          'vat': int(amount) - round(int(amount)/1.05),

                                          'total_amount_without_discount': int(amount_total) + int(shipping.shipping_fee),
                                          'subtotal_without_discount': round(int(amount_total)/1.05),
                                          'vat_without_discount': int(amount_total) - round(int(amount_total)/1.05),

                                          'total_with_shipping': int(amount) + int(shipping.shipping_fee)})
                return Response(data={'shipping_fee': '0',
                                      'delivery_time': delivery_date(int(shipping.delivery_day), city),
                                      'total_amount': int(amount),
                                      'subtotal': round(int(amount)/1.05),
                                      'vat': int(amount) - round(int(amount)/1.05),

                                      'total_amount_without_discount': int(amount_total) + 0,
                                      'subtotal_without_discount': round(int(amount_total)/1.05),
                                      'vat_without_discount': int(amount_total) - round(int(amount_total)/1.05),

                                      'total_with_shipping': int(amount) + 0
                                      })
            else:
                shipping = ShippingCountryModel.objects.get(country=country)
                if float(shipping.threshold_free) > amount:
                    return Response(data={'shipping_fee': shipping.shipping_fee,
                                          'delivery_time': delivery_date(int(shipping.delivery_day), city),
                                          'total_amount': int(amount),
                                          'subtotal': round(int(amount)/1.05),
                                          'vat': int(amount) - round(int(amount)/1.05),

                                          'total_amount_without_discount': int(amount_total) + int(shipping.shipping_fee),
                                          'subtotal_without_discount': round(int(amount_total)/1.05),
                                          'vat_without_discount': int(amount_total) - round(int(amount_total)/1.05),

                                          'total_with_shipping': int(amount) + int(shipping.shipping_fee)
                                          })
                return Response(data={'shipping_fee': '0',
                                      'delivery_time': delivery_date(int(shipping.delivery_day), city),
                                      'total_amount': int(amount),
                                      'subtotal': round(int(amount)/1.05),
                                      'vat': int(amount) - round(int(amount)/1.05),

                                      'total_amount_without_discount': int(amount_total) + 0,
                                      'subtotal_without_discount': round(int(amount_total)/1.05),
                                      'vat_without_discount': int(amount_total) - round(int(amount_total)/1.05),

                                      'total_with_shipping': int(amount) + 0
                                      })
        else:
            return Response(data={'shipping_fee': '300',
                                  'delivery_day': delivery_date(7),
                                  'total_amount': int(amount),
                                  'subtotal': round(int(amount)/1.05),
                                  'vat': int(amount) - round(int(amount)/1.05),

                                  'total_amount_without_discount': int(amount_total) + 300,
                                  'subtotal_without_discount': round(int(amount_total)/1.05),
                                  'vat_without_discount': int(amount_total) - round(int(amount_total)/1.05),

                                  'total_with_shipping': int(amount) + 300
                                  })


class TabbyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        forms = request.data['product']
        discount_code = request.data.get('discount_code', None)

        def shipping_fee(country, city, amount):
            if ShippingCountryModel.objects.filter(country=country).exists():
                country_model = ShippingCountryModel.objects.get(country=country)
                if ShippingModel.objects.filter(country=country_model, city=city).exists():
                    shipping = ShippingModel.objects.get(country=country_model, city=city)
                    if float(shipping.threshold_free) > amount:
                        return shipping.shipping_fee
                    return 0
                else:
                    shipping = ShippingCountryModel.objects.get(country=country)
                    if float(shipping.threshold_free) > amount:
                        return shipping.shipping_fee
                    return 0
            else:
                return 300

        if len(forms) > 0:
            address = get_object_or_404(AddressModel, id=request.data['address_id'])
            order = OrderModel.objects.create(user=request.user, address=address,
                                              status=OrderStatusModel.objects.get(status='New'))

            discount_percent = None
            discount_amount = None
            if discount_code:
                try:
                    code = CouponModel.objects.get(coupon_code=discount_code)
                    if code.is_valid() and code.active and (code.limit > 0 or code.infinite):
                        if code.discount_percent is not None and int(code.discount_percent) != 0:
                            discount_percent = int(code.discount_percent)
                        elif code.discount_amount is not None and int(code.discount_amount) != 0:
                            discount_amount = int(code.discount_amount)
                except:
                    code = None
            else:
                code = None

            for form in forms:
                product = ProductVariantModel.objects.get(id=form['product_id'])
                color = product.color
                size = product.size
                quantity = form['quantity']
                price = product.price
                discount_price = product.get_off_price()
                selling_price = product.get_off_price()
                if discount_code is not None:
                    try:
                        code = CouponModel.objects.get(coupon_code=discount_code)
                        if code.is_valid() and code.active and (code.limit > 0 or code.infinite):
                            if not code.extra_discount:
                                if discount_percent:
                                    selling_price = price - (price * discount_percent) / 100
                                elif discount_amount:
                                    selling_price = price
                            else:
                                if discount_percent:
                                    selling_price = discount_price - (discount_price * discount_percent) / 100
                                elif discount_amount:
                                    selling_price = discount_price
                    except:
                        code = None
                else:
                    code = None

                OrderItemModel.objects.create(order=order,
                                              user=request.user,
                                              product=product,
                                              price=price,
                                              discount_price=discount_price,
                                              selling_price=selling_price,
                                              quantity=quantity,
                                              color=color,
                                              size=size,)

            def total_price_without_discount():
                total_price = 0
                for frm in forms:
                    prd = ProductVariantModel.objects.get(id=frm['product_id'])
                    qnt = frm['quantity']
                    prc = prd.price
                    total_price += int(qnt) * int(prc)
                return total_price

            def total_price_with_discount():
                total_price = 0
                for frm in forms:
                    prd = ProductVariantModel.objects.get(id=frm['product_id'])
                    qnt = frm['quantity']
                    prc = prd.get_off_price()
                    total_price += int(qnt) * int(prc)
                return total_price

            total_price_without_discount = total_price_without_discount()
            total_price_with_discount = total_price_with_discount()

            if code and not code.extra_discount and int(code.discount_threshold) <= total_price_without_discount:
                if discount_percent:
                    amount = int(
                        total_price_without_discount - (total_price_without_discount * int(discount_percent)) / 100)
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
                elif discount_amount:
                    amount = int(total_price_without_discount - int(discount_amount))
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
            elif code and code.extra_discount and int(code.discount_threshold) <= total_price_with_discount:
                if discount_percent:
                    amount = int(total_price_with_discount - (total_price_with_discount * int(discount_percent)) / 100)
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
                elif discount_amount:
                    amount = int(total_price_with_discount - int(discount_amount))
                    amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))
            else:
                amount = int(str(order.get_total_price()))
                amount_shipping = amount + int(shipping_fee(address.country, address.city, amount))

            # Create Tabby payment session
            try:
                tabby = TabbyPayment(order.id)
                payment_session = tabby.create_payment_session()
                installments = (
                    payment_session.get('configuration', {})
                    .get('available_products', {})
                    .get('installments', [])
                )
                if installments and 'web_url' in installments[0]:
                    order.ref_id = payment_session.get('id', '')
                    order.cart_id = str(order.id)
                    order.coupon = code
                    order.total_discount = int(total_price_without_discount) - int(amount)
                    order.total_amount = amount
                    order.shipping = int(shipping_fee(address.country, address.city, amount))
                    order.save()
                    if code and not code.infinite:
                        code.limit -= 1
                        code.save()
                    return Response({
                        'status': 'success',
                        'payment_url': installments[0]['web_url']
                    })
                else:
                    return Response({
                        'status': 'error',
                        'message': 'ساختار پاسخ Tabby نامعتبر است',
                        'tabby_response': payment_session
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)


class TabbyPaymentSuccessView(APIView):
    def get(self, request):
        payment_id = request.GET.get('payment_id')
        order_id = request.GET.get('order_id')
        try:
            tabby = TabbyPayment(order_id)
            order = tabby.order
            if order.paid:
                return redirect(f'{settings.FRONTEND_URL}/payment/success/')
            if tabby.verify_payment(payment_id):
                # عملیات پرداخت و ارسال ایمیل فقط یک بار
                process_order_payment(order)
                return redirect(f'{settings.FRONTEND_URL}/payment/success/')
            return redirect(f'{settings.FRONTEND_URL}/payment/failure/')
        except Exception as e:
            return redirect(f'{settings.FRONTEND_URL}/payment/failure/')


class TabbyPaymentFailureView(APIView):
    def get(self, request):
        return redirect(f'{settings.FRONTEND_URL}/payment/failure/')


class TabbyPaymentCancelView(APIView):
    def get(self, request):
        payment_id = request.GET.get('payment_id')
        order_id = request.GET.get('order_id')
        
        try:
            tabby = TabbyPayment(order_id)
            tabby.cancel_payment(payment_id)
            return redirect(f'{settings.FRONTEND_URL}/payment/cancel/')
        except Exception as e:
            return redirect(f'{settings.FRONTEND_URL}/payment/cancel/')
