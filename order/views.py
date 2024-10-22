from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests
from .models import OrderModel, OrderItemModel, OrderStatusModel, ShippingModel, ShippingCountryModel
from product.models import ProductModel, ColorProductModel, SizeProductModel, ProductVariantModel, CouponModel
from order.models import UserProductModel
from accounts.models import AddressModel
from django.shortcuts import get_object_or_404
from .serializers import OrderUserSerializer
from django.core.mail import send_mail
from utils import send_order_email
from datetime import datetime, timedelta
import holidays


class OrderPayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        forms = request.data['product']
        discount_code = request.data.get('discount_code', None)

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
                elif discount_amount:
                    amount = int(total_price_without_discount - int(discount_amount))
            elif code and code.extra_discount and int(code.discount_threshold) <= total_price_with_discount:
                if discount_percent:
                    amount = int(total_price_with_discount - (total_price_with_discount * int(discount_percent)) / 100)
                elif discount_amount:
                    amount = int(total_price_with_discount - int(discount_amount))
            else:
                amount = str(order.get_total_price())

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
                    "amount": amount,
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
                    order.save()
                    request.session['ref_id'] = response['order']['ref']

                    if code and not code.infinite:
                        code.limit -= 1
                        code.save()
                    return Response({'redirect to : ': url}, status=200)
                else:
                    return Response({'Error code: ': str(response['error'])}, status=400)
            else:
                return Response({'details': str(response.json()['errors'])})


class OrderPayAuthorisedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # print(request.session.get('ref_id'))
        # print(request.user)
        # order = OrderModel.objects.get(ref_id=request.session.get('ref_id'))
        try:
            # order = OrderModel.objects.filter(user=user).first()
            order = OrderModel.objects.get(ref_id=request.session.get('ref_id'))
            print(order)
            order.error_note = 'Error 00'
            order.save()
        except:
            # return HttpResponseRedirect(redirect_to='https://gogle.com')
            print('order error')
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
        ## to do: if quantity = 0 dont send request

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
            order.paid = True
            order.save()
            order_items = order.items.all()

            for item in order_items:

                order.error_note = 'Error 04'
                order.save()

                product_variant = item.product
                price = product_variant.get_off_price()
                quantity = item.quantity

                product_variant.quantity = product_variant.quantity - quantity
                product_variant.save()

                item.trace = response['trace']
                item.save()

                order.error_note = 'Error 05'
                order.save()

                UserProductModel.objects.create(user=request.user, product=product_variant, order=order,
                                                quantity=quantity, price=price)

                order.error_note = 'Error 06'
                order.save()

            recipient_list = ['hamed.alizadegan@gmail.com', 'hamed@healfit.ae', order.user.email]
            send_order_email(order, order_items, recipient_list)

            # return HttpResponseRedirect(redirect_to='https://gogle.com')
            return Response(data={'message': 'success', 'cart_id': order.cart_id,
                                  'transaction_ref': transaction})

        else:
            order.paid = False
            order.trace = 'Eroor 07'
            order.error_message = 'Error 07'
            order.error_note = 'Eroor 07'

            order.save()
            # return HttpResponseRedirect(redirect_to='https://gogle.com')
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

        return Response(data={'message': 'Declined'})


class OrderPayCancelledView(APIView):
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
        if 'status' in response['order']:
            transaction = response['order']['status']['text']
        else:
            transaction = None

        order.paid = False
        order.trace = response['trace']
        order.transaction_ref = transaction
        order.error_message = 'cancelled'
        order.save()

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

        def holidays_count(start_date, end_date):
            uae_holidays = holidays.UnitedArabEmirates(years=datetime.now().year)

            count = 0

            while start_date <= end_date:
                if start_date in uae_holidays:
                    count += 1
                elif start_date.weekday() in (5, 6):
                    count += 1
                start_date += timedelta(days=1)

            return count

        def delivery_date(delivery_day, zone=None):

            order_time = datetime.now()
            work_time = datetime.strptime("17:00", '%H:%M')

            if order_time.time() > work_time.time():
                delivery_time = datetime.now() + timedelta(days=delivery_day + 1)
            else:
                delivery_time = datetime.now() + timedelta(days=delivery_day)

            if zone != 'Dubai':
                delivery_time += timedelta(days=holidays_count(order_time, delivery_time))

            return delivery_time.strftime('%Y-%m-%d')

        if ShippingCountryModel.objects.filter(country=country).exists():
            country_model = ShippingCountryModel.objects.get(country=country)
            if ShippingModel.objects.filter(country=country_model, city=city).exists():
                shipping = ShippingModel.objects.get(country=country_model, city=city)
                if float(shipping.threshold_free) > amount:
                    return Response(data={'shipping_fee': shipping.shipping_fee, 'delivery_time': delivery_date(int(shipping.delivery_day), city)})
                return Response(data={'shipping_fee': '0', 'delivery_time': delivery_date(int(shipping.delivery_day), city)})
            else:
                shipping = ShippingCountryModel.objects.get(country=country)
                if float(shipping.threshold_free) > amount:
                    return Response(data={'shipping_fee': shipping.shipping_fee, 'delivery_time': delivery_date(int(shipping.delivery_day), city)})
                return Response(data={'shipping_fee': '0', 'delivery_time': delivery_date(int(shipping.delivery_day), city)})
        else:
            return Response(data={'shipping_fee': '0', 'delivery_day': ''})  # delivery_date(7)
