from django.conf import settings
from accounts.models import User
import requests
from datetime import datetime


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
                   # "status": "paid",
                   "notes": "Looking forward for your business.",
                   "is_inclusive_tax": True,
                   "line_items": line_items,
                   }

        response_item = requests.post(url=url_invoice, headers=headers, json=payload)
        response_item = response_item.json()

        print(response_item)

        # --- Add payment to mark invoice as paid ---
        if 'invoice' in response_item and 'invoice_id' in response_item['invoice']:
            invoice_id = response_item['invoice']['invoice_id']
            invoice_total = response_item['invoice']['total']
            url_payment = f'https://www.zohoapis.com/books/v3/customerpayments?organization_id={organization_id}'
            payment_payload = {
                "customer_id": customer_id,
                "payment_mode": "creditcard",
                "amount": invoice_total,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "invoices": [
                    {
                        "invoice_id": invoice_id,
                        "amount_applied": invoice_total
                    }
                ],
                "invoice_id": invoice_id,
                "amount_applied": invoice_total,

            }
            payment_response = requests.post(url=url_payment, headers=headers, json=payment_payload)
            payment_response = payment_response.json()
            response_item['payment'] = payment_response

        return response_item
    else:
        return response_item
