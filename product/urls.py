from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('gender_home/', views.ProductGenderView.as_view(), name='gender_home'),
    path('gender/', views.ProductGenderListView.as_view(), name='product_list'),
    path('all/', views.ProductAllView.as_view(), name='product_all'),

    # Category
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/items/<slug:slug_category>/', views.CategoryItemView.as_view(), name='category_item'),
    path('category/<int:category_id>/', views.CategoryFilterView.as_view(), name='category'),
    path('category/subcategories/<int:category_id>/', views.CategoryBySubcategoryView.as_view(), name='category_subcategory'),

    # Subcategory
    path('subcategories/', views.SubcategoryListView.as_view(), name='subcategory_list'),
    path('subcategory/items/<slug:slug_subcategory>/', views.SubcategoryItemView.as_view(), name='subcategory_item'),
    path('subcategory/<int:subcategory_id>/', views.SubcategoryFilterView.as_view(), name='subcategory'),

    # Shop
    path('items/<slug:product>/', views.ProductItemView.as_view(), name='product_item'),

]
