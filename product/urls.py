from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('gender_home/', views.ProductGenderView.as_view(), name='gender_home'),
    path('gender/', views.ProductGenderListView.as_view(), name='product_list'),
    path('all/', views.ProductAllView.as_view(), name='product_all'),
    path('fav/', views.FavProductView.as_view(), name='fav_product'),
    path('fav/<int:product_id>/', views.FavProductView.as_view(), name='fav_item'),
    path('user/fav/', views.UserFavView.as_view(), name='fav_user'),
    path('custom_made/', views.CustomMadeView.as_view(), name='custom_made'),
    path('custom_made_page/', views.CustomMadePageView.as_view(), name='custom_made_page'),
    path('brand_page/<int:brand_id>/', views.BrandPageView.as_view(), name='brand_page'),

    # Category
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/items/<slug:slug_category>/', views.CategoryItemView.as_view(), name='category_item'),
    path('category/<slug:slug_category>/', views.CategoryFilterView.as_view(), name='category'),
    path('category/subcategories/<slug:slug_category>/', views.CategoryBySubcategoryView.as_view(), name='category_subcategory'),
    path('categories/best_seller/', views.CategoryBestSellerView.as_view(), name='category_best_seller'),

    # Subcategory
    path('subcategories/', views.SubcategoryListView.as_view(), name='subcategory_list'),
    path('subcategory/items/<slug:slug_subcategory>/', views.SubcategoryItemView.as_view(), name='subcategory_item'),
    path('subcategory/<slug:slug_subcategory>/', views.SubcategoryFilterView.as_view(), name='subcategory'),

    # Shop
    path('items/<slug:slug_product>/', views.ProductItemView.as_view(), name='product_item'),
    path('get_class/<slug:slug_product>/', views.GetClassView.as_view(), name='get_class'),

    path('new_items/<slug:slug_product>/', views.ProductNewItemView.as_view(), name='product_new_item'),

    path('variant/', views.ProductVariantShopView.as_view(), name='product_variant'),
    path('colorimage/', views.ProductColorImageView.as_view(), name='color_image'),
    path('sizeofcolor/', views.SizeOfColorView.as_view(), name='size_of_color'),
    path('search_product/', views.SearchProductView.as_view({'get': 'list'}), name='search_product'),

    # Cart
    path('cart/', views.CartView.as_view(), name='cart'),
]
