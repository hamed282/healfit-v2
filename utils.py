from django.conf import settings
import requests
from accounts.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from home.models import TelegramBotModel


def zoho_refresh_token(scope):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    grant_type = settings.GRANT_TYPE
    scope = scope
    soid = settings.SIOD

    url_refresh_token = f'https://accounts.zoho.com/oauth/v2/token?client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}&scope={scope}&soid={soid}'
    response_refresh_token = requests.post(url=url_refresh_token)
    response_refresh_token = response_refresh_token.json()
    response_refresh = response_refresh_token['access_token']

    return response_refresh


def zoho_invoice_quantity_update(first_name, last_name, email, address, city, line_items,
                                 country='United Arab Emirates', customer_id=None):

    organization_id = settings.ORGANIZATION_ID
    if not customer_id:
        oauth = zoho_refresh_token(settings.SCOPE_BOOK_CONTACTS)
        try:
            headers = {
                'Authorization': f"Zoho-oauthtoken {oauth}",
                'content-type': "application/json"}

            payload = {'contact_name': f'{first_name} {last_name}',
                        'billing_address': {
                            "address": address,
                            "city": city,
                            "country": country,
                        },
                       'shipping_address': {
                           "address": address,
                           "city": city,
                           "country": country,
                       },
                       }
            url_contact = f'https://www.zohoapis.com/books/v3/contacts?organization_id={organization_id}'
            url_contact_person = f'https://www.zohoapis.com/books/v3/contacts/contactpersons?organization_id={organization_id}'

            response_item = requests.post(url=url_contact, headers=headers, json=payload)
            response_item = response_item.json()

            customer_id = response_item['contact']['contact_id']
            payload = {"contact_id": customer_id,
                       # 'salutation': 'Mr.',
                       "first_name": first_name,
                       "last_name": last_name,
                       'email': email}

            response_item = requests.post(url=url_contact_person, headers=headers, json=payload)
            response_item = response_item.json()

            user = User.objects.get(email=email)
            user.zoho_customer_id = customer_id
            user.save()
        except:
            headers = {
                'Authorization': f"Zoho-oauthtoken {oauth}",
                'content-type': "application/json"}

            payload = {'contact_name': f'{first_name} {last_name} 2',
                       'billing_address': {
                           "address": address,
                           "city": city,
                           "country": country,
                       },
                       'shipping_address': {
                           "address": address,
                           "city": city,
                           "country": country,
                       },
                       }
            url_contact = f'https://www.zohoapis.com/books/v3/contacts?organization_id={organization_id}'
            url_contact_person = f'https://www.zohoapis.com/books/v3/contacts/contactpersons?organization_id={organization_id}'

            response_item = requests.post(url=url_contact, headers=headers, json=payload)
            response_item = response_item.json()

            customer_id = response_item['contact']['contact_id']
            payload = {"contact_id": customer_id,
                       # 'salutation': 'Mr.',
                       "first_name": first_name,
                       "last_name": last_name,
                       'email': email}

            response_item = requests.post(url=url_contact_person, headers=headers, json=payload)
            response_item = response_item.json()

            user = User.objects.get(email=email)
            user.zoho_customer_id = customer_id
            user.save()

    else:
        customer_id = customer_id
        response_item = {'code': 0}

    if response_item['code'] == 0:
        # customer_id = response_item['contact']['contact_id']
        url_invoice = f'https://www.zohoapis.com/books/v3/invoices?organization_id={organization_id}'

        oauth = zoho_refresh_token(settings.SCOPE_BOOK_INVOICE)
        headers = {
            'Authorization': f"Zoho-oauthtoken {oauth}",
            'content-type': "application/json"}

        payload = {'customer_id': customer_id,
                   "status": "paid",
                   "notes": "Looking forward for your business.",
                   'line_items': line_items,
                   }

        response_item = requests.post(url=url_invoice, headers=headers, json=payload)
        response_item = response_item.json()
        return response_item
    else:
        return response_item


def send_order_email(order, order_items, recipient_list):
    subject = 'Your Order Has been Received'

    products = [{'name': item.product.name,
                'quantity': item.quantity,
                'amount': item.selling_price,
                'taxable_amount': round(int(item.selling_price)/1.05, 2),
                'tax_amount': round(int(item.selling_price) - round(int(item.selling_price)/1.05, 2), 2),
                } for item in order_items]

    context = {'invoice_number': f'E-INV-{str(order.created.year)[-2:]}-{str(order.cart_id).zfill(6)}',
               'bill_to': {'name': f'{order.user.first_name} {order.user.last_name}',
                           'address': f'{order.address.address}',
                           'city': f'{order.address.city}',
                           'country': f'{order.address.country}'},
               'invoice_date': order.created.strftime("%d-%m-%Y"),
               'products': products,
               'total_invoice': sum(int(item.selling_price) * int(item.quantity) for item in order_items) + int(order.shipping),
               'shipping_fee': order.shipping,
               'total_taxable_amount': sum(round(int(item.selling_price)/1.05, 2) * int(item.quantity) for item in order_items),
               'total_tax_amount': sum(round(int(item.selling_price) - round(int(item.selling_price)/1.05, 2), 2) * int(item.quantity) for item in order_items)
               }

    # قالب HTML را با استفاده از render_to_string رندر می‌کنیم
    html_content = render_to_string('invoice/invoice.html', context=context)

    # محتوای ساده (متن) ایمیل برای نسخه‌هایی که از HTML پشتیبانی نمی‌کنند
    text_content = f'New Order Received \n' \
                   f'Customer Name: {order.user} \n' \
                   f'Transaction Reference: {order.transaction_ref} \n' \
                   f'Cart Id: {order.cart_id}'

    email_from = settings.EMAIL_HOST_USER
    # recipient_list = ['hamed.alizadegan@gmail.com']

    # ایجاد ایمیل
    email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)

    # اضافه کردن نسخه HTML
    email.attach_alternative(html_content, "text/html")

    # ارسال ایمیل
    email.send()


def send_order_telegram(order, order_items):
    token = '7634802186:AAEXRh2YALEoXZXDA6TywGckdG_7erAgrxA'
    bill_to = {'name': f'{order.user.first_name} {order.user.last_name}',
               'address': f'{order.address.address}',
               'city': f'{order.address.city}',
               'country': f'{order.address.country}'}

    products = [{'name': item.product.name,
                'quantity': item.quantity,
                'amount': item.selling_price,
                'taxable_amount': round(int(item.selling_price)/1.05, 2),
                'tax_amount': round(int(item.selling_price) - round(int(item.selling_price)/1.05, 2), 2),
                } for item in order_items]

    total_invoice = sum(int(item.selling_price) * int(item.quantity) for item in order_items) + int(order.shipping),
    shipping_fee = order.shipping,
    product_message = ''
    id_message = 1
    for product in products:
        product_message += f"{id_message}- {product['name']} - {product['quantity']} pcs - {product['amount']} AED \n"
        id_message += 1

    message = ('New Order Received\n \n'
               f"Bill to: {bill_to['name']} - {bill_to['address']} - {bill_to['city']} - {bill_to['country']}\n \n"
               f'Products: \n {product_message} \n \n'
               f'shipping fee: {shipping_fee[0]} \n'
               f'total amount: {total_invoice[0]}')

    chat_list = TelegramBotModel.objects.all()
    chat_list = [chat_id for chat_id in chat_list]
    for chat_id in chat_list:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
        response = requests.get(url)
        print(response.json())


