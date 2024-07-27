from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('gender_home/', views.ProductGenderView.as_view(), name='gender_home'),
    path('gender/', views.ProductGenderListView.as_view(), name='product_list'),
    path('all/', views.ProductAllView.as_view(), name='product_all'),
    path('category/<int:category_id>/', views.CategoryItemView.as_view(), name='category_items'),

]
