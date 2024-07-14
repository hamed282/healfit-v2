from django.urls import path
from . import views


app_name = 'admin_panel'
urlpatterns = [
    path('user/', views.UserView.as_view(), name='users'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user_id'),
    path('user/all/', views.UserValueView.as_view(), name='user_all'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('login/', views.LoginUserView.as_view(), name='login'),
]
