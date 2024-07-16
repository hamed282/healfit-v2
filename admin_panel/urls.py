from django.urls import path
from . import views


app_name = 'admin_panel'
urlpatterns = [
    path('user/', views.UserView.as_view(), name='users'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user_id'),
    path('user/all/', views.UserValueView.as_view(), name='user_all'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('language/active/', views.LanguageView.as_view(), name='language'),
    path('blog/list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:blog_id>/', views.BlogView.as_view(), name='blog_item_get'),
    path('blog/item/', views.BlogView.as_view(), name='blog_item'),
]
