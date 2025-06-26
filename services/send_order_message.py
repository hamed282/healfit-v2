from django.conf import settings
import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from home.models import TelegramBotModel


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
               'total_invoice': sum(int(item.selling_price) * int(item.quantity)
                                    for item in order_items) + int(order.shipping),
               'shipping_fee': order.shipping,
               'total_taxable_amount': sum(round(int(item.selling_price)/1.05, 2) * int(item.quantity)
                                           for item in order_items),
               'total_tax_amount': sum(round(int(item.selling_price) - round(int(item.selling_price)/1.05, 2), 2)
                                       * int(item.quantity) for item in order_items)
               }

    html_content = render_to_string('invoice/invoice.html', context=context)

    text_content = f'New Order Received \n' \
                   f'Customer Name: {order.user} \n' \
                   f'Transaction Reference: {order.transaction_ref} \n' \
                   f'Cart Id: {order.cart_id}'

    email_from = settings.EMAIL_HOST_USER
    
    # Split the recipient list - customer email is the main recipient, others go to BCC
    customer_email = recipient_list[-1]  # Last email is the customer's email
    bcc_list = recipient_list[:-1]  # All other emails go to BCC

    email = EmailMultiAlternatives(subject, text_content, email_from, [customer_email], bcc=bcc_list)

    # اضافه کردن نسخه HTML
    email.attach_alternative(html_content, "text/html")

    # ارسال ایمیل
    email.send()


def send_inprocess_email(order, recipient_list):
    subject = 'Your Order Has been Received'

    # محتوای ساده (متن) ایمیل برای نسخه‌هایی که از HTML پشتیبانی نمی‌کنند
    text_content = f'order {order.transaction_ref} is in process'

    email_from = settings.EMAIL_HOST_USER

    # ایجاد ایمیل
    email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)

    # ارسال ایمیل
    email.send()


def send_order_telegram(order, order_items):
    token = '7634802186:AAEXRh2YALEoXZXDA6TywGckdG_7erAgrxA'
    bill_to = {'name': f'{order.user.first_name} {order.user.last_name}',
               'address': f'{order.address.address}',
               'city': f'{order.address.city}',
               'country': f'{order.address.country}',
               'email': f'{order.user.email}',
               'phone': f'{order.address.phone_number}',
               'ref_id': f'{order.ref_id}',
               'order_id': f'{order.cart_id}'}

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
               f"Bill to: name: {bill_to['name']} - address: {bill_to['address']} -  city: {bill_to['city']} - country: {bill_to['country']}"
               f" - email: {bill_to['email']} - phone: {bill_to['phone']} - reference id: {bill_to['ref_id']} - order id: {bill_to['order_id']}\n \n"
               f'Products: \n {product_message} \n \n'
               f'shipping fee: {shipping_fee[0]} \n'
               f'total amount: {total_invoice[0]}')

    chat_list = TelegramBotModel.objects.all()
    chat_list = [chat_id for chat_id in chat_list]
    for chat_id in chat_list:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
        response = requests.get(url)
        print(response.json())


def send_custom_made_email(recipient_list):
    subject = 'Your Form Has been Received'

    # context = {'invoice_number': f'E-INV-{str(order.created.year)[-2:]}-{str(order.cart_id).zfill(6)}',
    #            'bill_to': {'name': f'{order.user.first_name} {order.user.last_name}',
    #                        'address': f'{order.address.address}',
    #                        'city': f'{order.address.city}',
    #                        'country': f'{order.address.country}'},
    #            'invoice_date': order.created.strftime("%d-%m-%Y"),
    #            'products': products,
    #            'total_invoice': sum(int(item.selling_price) * int(item.quantity)
    #                                 for item in order_items) + int(order.shipping),
    #            'shipping_fee': order.shipping,
    #            'total_taxable_amount': sum(round(int(item.selling_price) / 1.05, 2) * int(item.quantity)
    #                                        for item in order_items),
    #            'total_tax_amount': sum(round(int(item.selling_price) - round(int(item.selling_price) / 1.05, 2), 2)
    #                                    * int(item.quantity) for item in order_items)
    #            }

    # html_content = render_to_string('invoice/invoice.html', context=context)

    text_content = f'New Form Received'

    email_from = settings.EMAIL_HOST_USER

    # Split the recipient list - customer email is the main recipient, others go to BCC
    customer_email = recipient_list[-1]  # Last email is the customer's email
    bcc_list = recipient_list[:-1]  # All other emails go to BCC

    email = EmailMultiAlternatives(subject, text_content, email_from, [customer_email], bcc=bcc_list)

    # اضافه کردن نسخه HTML
    # email.attach_alternative(html_content, "text/html")

    # ارسال ایمیل
    email.send()


def send_custom_made_telegram():
    token = '7634802186:AAEXRh2YALEoXZXDA6TywGckdG_7erAgrxA'
    # bill_to = {'name': f'{order.user.first_name} {order.user.last_name}',
    #            'address': f'{order.address.address}',
    #            'city': f'{order.address.city}',
    #            'country': f'{order.address.country}',
    #            'email': f'{order.user.email}',
    #            'phone': f'{order.address.phone_number}',
    #            'ref_id': f'{order.ref_id}',
    #            'order_id': f'{order.cart_id}'}
    #
    # products = [{'name': item.product.name,
    #              'quantity': item.quantity,
    #              'amount': item.selling_price,
    #              'taxable_amount': round(int(item.selling_price)/1.05, 2),
    #              'tax_amount': round(int(item.selling_price) - round(int(item.selling_price)/1.05, 2), 2),
    #              } for item in order_items]

    message = 'New Form Received'

    chat_list = TelegramBotModel.objects.all()
    chat_list = [chat_id for chat_id in chat_list]
    for chat_id in chat_list:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
        response = requests.get(url)
        print(response.json())

# from order.models import OrderModel
# order = OrderModel.objects.filter(user=1).first()
# order_items = order.items.all()
# recipient_list = ['hamed.alizadegan@gmail.com']
# send_order_email(order, order_items, recipient_list)
