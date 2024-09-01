from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('auth/google/', views.GoogleLoginView.as_view(), name='google_login'),
    path('auth/apple/', views.AppleLoginView.as_view(), name='apple_login'),

    path('address/', views.UserAddressView.as_view(), name='user_address'),
    path('address/<int:address_id>/', views.UserAddressView.as_view(), name='user_address'),
    path('address/item/<int:address_id>/', views.UserAddressItemView.as_view(), name='user_address'),
    path('currentaddress/<int:user_id>/', views.CurrentAddressView.as_view(), name='cureent_address'),
    path('currentaddress/', views.CurrentAddressView.as_view(), name='current_address_create'),

    path('info/', views.UserInfoView.as_view(), name='user_info'),
    path('info/<int:user_id>/', views.UserInfoView.as_view(), name='user_info'),
]
