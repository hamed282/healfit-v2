from django.conf import settings
import requests
from accounts.models import User


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


def zoho_invoice_quantity_update(first_name,
                                 last_name,
                                 email,
                                 address,
                                 city,
                                 line_items,
                                 country='United Arab Emirates',
                                 customer_id=None):

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
            print(response_item['contact']['contact_id'])
            payload = {"contact_id": customer_id,
                       # 'salutation': 'Mr.',
                       "first_name": first_name,
                       "last_name": last_name,
                       'email': email}

            response_item = requests.post(url=url_contact_person, headers=headers, json=payload)
            response_item = response_item.json()

            print(response_item)
            user = User.objects.get(email=email)
            user.zoho_customer_id = customer_id
            user.save()
            print('not customer id')
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
            print(response_item['contact']['contact_id'])
            payload = {"contact_id": customer_id,
                       # 'salutation': 'Mr.',
                       "first_name": first_name,
                       "last_name": last_name,
                       'email': email}

            response_item = requests.post(url=url_contact_person, headers=headers, json=payload)
            response_item = response_item.json()

            print(response_item)
            user = User.objects.get(email=email)
            user.zoho_customer_id = customer_id
            user.save()
            print('not customer id 2')

    else:
        customer_id = customer_id
        response_item = {'code': 0}
        print(customer_id)
    ###################################

    if response_item['code'] == 0:
        print('*'*100)
        # print(response_item['contact']['contact_id'])
        # customer_id = response_item['contact']['contact_id']
        url_invoice = f'https://www.zohoapis.com/books/v3/invoices?organization_id={organization_id}'

        oauth = zoho_refresh_token(settings.SCOPE_BOOK_INVOICE)
        headers = {
            'Authorization': f"Zoho-oauthtoken {oauth}",
            'content-type': "application/json"}

        payload = {'customer_id': customer_id,
                   'line_items': line_items,
                   #     [
                   #     {
                   #         'item_id': item_id,
                   #         # 'name': 'Hard Drive',
                   #         # 'description': '',
                   #         # 'rate': 120,
                   #         'quantity': quantity,
                   #         # 'unit': " ",
                   #         # "tax_id": 982000000557028,
                   #         # "tds_tax_id": "982000000557012",
                   #         # "tax_name": "VAT",
                   #         # "tax_type": "tax",
                   #         # "tax_percentage": 12.5,
                   #         # "tax_treatment_code": "uae_others",
                   #     },
                   #     {
                   #         'item_id': 982000000030049,
                   #     }
                   # ],
                   }

        response_item = requests.post(url=url_invoice, headers=headers, json=payload)
        response_item = response_item.json()
        print('!'*100)
        print(response_item)
        return response_item
    else:
        return response_item

