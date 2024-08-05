from django.urls import path
from . import views


app_name = 'admin_panel'
urlpatterns = [
    # Accounts
    path('user/', views.UserView.as_view(), name='users'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user_id'),
    path('user/all/', views.UserValueView.as_view(), name='user_all'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('login/', views.LoginUserView.as_view(), name='login'),

    # General
    path('language/active/', views.LanguageView.as_view(), name='language'),

    # Blog
    path('blog/list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:blog_id>/', views.BlogView.as_view(), name='blog_item_get'),
    path('blog/item/', views.BlogView.as_view(), name='blog_item'),
    path('blog/image/', views.BlogImageView.as_view(), name='blog_image'),

    # Blog Tag
    path('blog/tag/', views.BLogTagListView.as_view(), name='tag_list'),
    path('blog/tag/<int:tag_id>/', views.BLogTagListView.as_view(), name='tag_create'),
    path('blog/tag/item/<int:tag_id>/', views.BLogTagItemView.as_view(), name='tag_item'),

    # Add Blog Tag
    path('blog/addtag/', views.AddBLogTagListView.as_view(), name='addtag_post'),
    path('blog/addtag/<int:blog_id>/', views.AddBLogTagListView.as_view(), name='addtag'),

    # Blog Category
    path('blog/category/', views.BlogCategoryView.as_view(), name='category'),
    path('blog/category/<int:category_id>/', views.BlogCategoryView.as_view(), name='category_put'),

    # Home
    path('home/comment/', views.CommentHomeView.as_view(), name='comment'),
    path('home/comment/item/', views.CommentItemView.as_view(), name='comment_item'),
    path('home/comment/item/<int:comment_id>/', views.CommentItemView.as_view(), name='comment_id'),

    path('home/banner/', views.BannerHomeView.as_view(), name='banner'),
    path('home/banner/item/', views.BannerItemView.as_view(), name='banner_item'),
    path('home/banner/item/<int:banner_id>/', views.BannerItemView.as_view(), name='banner_id'),

    path('home/video/', views.VideoHomeView.as_view(), name='video'),
    # path('home/video/item/', views.VideoItemView.as_view(), name='video_item'),
    path('home/video/item/<int:video_id>/', views.VideoHomeView.as_view(), name='video_id'),

    # Category
    path('product/category/', views.ProductCategoryView.as_view(), name='product_category'),
    path('product/category/item/', views.ProductCategoryItemView.as_view(), name='category_item'),
    path('product/category/item/<int:category_id>/', views.ProductCategoryItemView.as_view(), name='category_id'),

    # Subcategory
    path('product/subcategory/', views.ProductSubCategoryView.as_view(), name='product_subcategory'),
    path('product/subcategory/item/', views.ProductSubCategoryItemView.as_view(), name='subcategory_item'),
    path('product/subcategory/item/<int:category_id>/', views.ProductSubCategoryItemView.as_view(), name='subcategory_id'),

    # Extra
    path('extrag/all/', views.ExtraItemView.as_view(), name='extrag'),
    path('extrag/', views.ExtraGroupView.as_view(), name='extrag_item'),
    path('extrag/<int:id_extrag>/', views.ExtraGroupView.as_view(), name='extrag_item'),

    # Size
    path('size/<int:size_id>/', views.SizeItemView.as_view(), name='size_item'),
    path('size/value/', views.SizeValueView.as_view(), name='size_value'),
    path('size/value/<int:id_size>/', views.SizeValueView.as_view(), name='size_value_put'),

    # Color
    path('color/<int:color_id>/', views.ColorItemView.as_view(), name='color_item'),
    path('color/value/', views.ColorValueView.as_view(), name='color_value'),
    path('color/value/<int:id_color>/', views.ColorValueView.as_view(), name='color_value_put'),

    # Product
    path('products/', views.ProductView.as_view(), name='product'),
    path('product/item/<int:product_id>/', views.ProductItemView.as_view(), name='product'),
    path('product/item/', views.ProductItemView.as_view(), name='product'),
    path('product/genders/', views.GenderView.as_view(), name='gender'),

    # Product Tag
    path('product/tag/', views.ProductTagListView.as_view(), name='product_list'),
    path('product/tag/<int:product_id>/', views.ProductTagListView.as_view(), name='product_create'),
    path('product/tag/item/<int:product_id>/', views.ProductTagItemView.as_view(), name='product_item'),

    # Add Product Tag
    path('product/addtag/', views.AddProductTagListView.as_view(), name='addtag_post_product'),
    path('product/addtag/<int:product_id>/', views.AddProductTagListView.as_view(), name='addtag_product'),

    # Variant Product
    path('product/variant/', views.ProductVariantView.as_view(), name='variant_product'),

]
