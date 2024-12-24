import requests
from .models import ProductModel, ProductVariantModel, ColorProductModel, SizeProductModel
from celery import shared_task
from django.conf import settings
from services.zoho_services import zoho_refresh_token
from django.db import models


@shared_task
def zoho_product_update():
    organization_id = settings.ORGANIZATION_ID
    oauth = zoho_refresh_token(settings.SCOPE_READING)
    per_page = '200'
    headers = {
        'Authorization': f"Zoho-oauthtoken {oauth}"}

    has_more_page = True
    page = 0
    i = 1
    while has_more_page:
        page += 1
        url_itemgroups = f'https://www.zohoapis.com/inventory/v1/itemgroups?organization_id={organization_id}&page={page}&per_page={per_page}'

        response_itemgroups = requests.get(url=url_itemgroups, headers=headers)
        response_itemgroups = response_itemgroups.json()

        for item in response_itemgroups['itemgroups']:
            try:
                product = item['group_name'].strip()
                group_id = item['group_id']

                product_exists = ProductModel.objects.filter(product=product)

                if product_exists.exists():
                    product_obj = product_exists.get(product=product)
                    product_obj.price = item['items'][0]['rate']
                    product_obj.priority = ProductModel.objects.aggregate(max_priority=models.Max('priority'))['max_priority'] + 1
                    product_obj.save()

                else:
                    ProductModel.objects.create(product=product, group_id=group_id, price=item['items'][0]['rate'])  # price=item['price']
                i += 1
            except:
                continue
        has_more_page = response_itemgroups['page_context']['has_more_page']

    has_more_page = True
    page = 0
    i = 1
    while has_more_page:
        page += 1
        url_items = f'https://www.zohoapis.com/inventory/v1/items?organization_id={organization_id}&page={page}&per_page={per_page}'

        response_items = requests.get(url=url_items, headers=headers)
        response_items = response_items.json()

        for item in response_items['items']:

            try:
                product = item['group_name']

                product = ProductModel.objects.get(product=product)

                name = item['name']

                if item['attribute_name1'] == 'Color':
                    color = item['attribute_option_name1'].lower()
                    color = ColorProductModel.objects.get(color=color)

                    size = item['attribute_option_name2']
                    size = SizeProductModel.objects.get(size=size)
                else:
                    color = 'not color'
                    color = ColorProductModel.objects.get(color=color)

                    size = item['attribute_option_name1']
                    size = SizeProductModel.objects.get(size=size)

                quantity = item['stock_on_hand']
                item_id = item['item_id']
                price = item['rate']
                product_variant = ProductVariantModel.objects.filter(name=name)
                if product_variant.exists():
                    product_obj = product_variant.get(name=name)
                    product_obj.quantity = quantity
                    product_obj.price = price
                    product_obj.save()

                else:
                    ProductVariantModel.objects.create(product=product,
                                                       name=name,
                                                       item_id=item_id,
                                                       color=color,
                                                       size=size,
                                                       price=price,
                                                       quantity=quantity)
                i += 1
            except:
                product = item['group_name']
                continue

        has_more_page = response_items['page_context']['has_more_page']
