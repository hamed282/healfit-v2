from django.conf import settings

TABBY_CONFIG = {
    'API_KEY': settings.TABBY_API_KEY,
    'API_URL': 'https://api.tabby.ai/api/v2/',
    'MERCHANT_CODE': settings.TABBY_MERCHANT_CODE,
    'CURRENCY': 'AED',
    'MIN_AMOUNT': 100,
    'MAX_AMOUNT': 50000,
    # 'SUCCESS_URL': f'{settings.SITE_URL}/payment/tabby/success/',
    # 'FAILURE_URL': f'{settings.SITE_URL}/payment/tabby/failure/',
    # 'CANCEL_URL': f'{settings.SITE_URL}/payment/tabby/cancel/',
    'SUCCESS_URL': f'{settings.SITE_URL}/authorised//',
    'FAILURE_URL': f'{settings.SITE_URL}/declined/',
    'CANCEL_URL': f'{settings.SITE_URL}/cancelled/',
}
