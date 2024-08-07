from django.urls import path
from . import views


app_name = 'order'
urlpatterns = [
    path('pay/', views.OrderPayView.as_view(), name='pay'),
    # path('pay/verify/', views.OrderPayVerifyView.as_view(), name='verify_pay'),
    path('authorised/', views.OrderPayAuthorisedView.as_view(), name='authorised_pay'),
    # path('authorised/', views.OrderPayAuthorisedView.as_view(), name='authorised_pay'),
    path('declined/', views.OrderPayDeclinedView.as_view(), name='declined_pay'),
    path('cancelled/', views.OrderPayCancelledView.as_view(), name='declined_pay'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
]

