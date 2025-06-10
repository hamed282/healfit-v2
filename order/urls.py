from django.urls import path
from . import views


app_name = 'order'
urlpatterns = [
    path('pay/', views.OrderPayView.as_view(), name='pay'),
    path('authorised/', views.OrderPayAuthorisedView.as_view(), name='authorised_pay'),
    path('declined/', views.OrderPayDeclinedView.as_view(), name='declined_pay'),
    path('cancelled/', views.OrderPayCancelledView.as_view(), name='declined_pay'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('shipping/', views.ShippingView.as_view(), name='shipping'),
    path('tabby/payment/', views.TabbyPaymentView.as_view(), name='tabby_payment'),
    path('tabby/payment/success/', views.TabbyPaymentSuccessView.as_view(), name='tabby_payment_success'),
    path('tabby/payment/failure/', views.TabbyPaymentFailureView.as_view(), name='tabby_payment_failure'),
    path('tabby/payment/cancel/', views.TabbyPaymentCancelView.as_view(), name='tabby_payment_cancel'),
]

