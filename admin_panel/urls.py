from django.urls import path
from . import views


app_name = 'admin_panel'
urlpatterns = [
    # Accounts
    path('user/', views.UserView.as_view(), name='users'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user_id'),
    path('user/<int:user_id>/role/update/', views.RoleUpdateView.as_view(), name='user_id'),
    path('user/all/', views.UserValueView.as_view(), name='user_all'),
    path('change_password/<int:user_id>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('login/', views.LoginUserView.as_view(), name='login'),

    # General
    path('language/active/', views.LanguageView.as_view(), name='language'),
    path('image_remove/<int:product_id>/<str:image_field>/', views.ImageDeleteView.as_view(), name='remove_image'),

    # Blog
    path('blog/list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:blog_id>/', views.BlogView.as_view(), name='blog_item_get'),
    path('blog/item/', views.BlogView.as_view(), name='blog_item'),
    path('blog/image/', views.BlogImageView.as_view(), name='blog_image'),
    path('search_blog/', views.SearchBlogView.as_view({'get': 'list'}), name='search_blog'),

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

    # Blog Author
    path('blog/author/', views.BlogAuthorView.as_view(), name='author'),
    path('blog/author/<int:author_id>/', views.BlogAuthorItemView.as_view(), name='author_put'),

    # Blog Comment
    path('blog/comments/', views.BlogCommentsView.as_view(), name='blog_comments'),
    path('blog/comment/edit/<int:comment_id>/', views.BlogCommentEditView.as_view(), name='blog_comments'),
    path('blog/search_comment/', views.SearchBlogCommentView.as_view({'get': 'list'}), name='search_comment'),
    path('blog/comments/notif', views.BlogCommentsNotifView.as_view(), name='comments_notif'),

    # Home
    path('home/comment/', views.CommentHomeView.as_view(), name='comment'),
    path('home/comment/item/', views.CommentItemView.as_view(), name='comment_item'),
    path('home/comment/item/<int:comment_id>/', views.CommentItemView.as_view(), name='comment_id'),

    path('home/banner/', views.BannerHomeView.as_view(), name='banner'),
    path('home/banner/item/', views.BannerItemView.as_view(), name='banner_item'),
    path('home/banner/item/<int:banner_id>/', views.BannerItemView.as_view(), name='banner_id'),

    path('home/banner_mobile/', views.BannerMobileHomeView.as_view(), name='banner_mobile'),
    path('home/banner_mobile/item/', views.BannerMobileItemView.as_view(), name='banner_item_mobile'),
    path('home/banner_mobile/item/<int:banner_id>/', views.BannerMobileItemView.as_view(), name='banner_id_mobile'),

    path('home/video/', views.VideoHomeView.as_view(), name='video'),
    path('home/video/item/<int:video_id>/', views.VideoHomeView.as_view(), name='video_id'),

    path('home/content1/', views.HomeContent1View.as_view(), name='content'),
    # path('home/content1/<int:content_id>/', views.HomeContentView.as_view(), name='content_id'),

    path('home/content2/', views.HomeContent2View.as_view(), name='content'),
    # path('home/content2/<int:content_id>/', views.HomeContentView.as_view(), name='content_id'),

    path('home/content3/', views.HomeContent3View.as_view(), name='content'),
    # path('home/content3/<int:content_id>/', views.HomeContentView.as_view(), name='content_id'),

    path('home/contactus/', views.ContactUsView.as_view(), name='contactus'),
    path('home/contactus/<int:contact_id>/', views.ContactUsItemView.as_view(), name='contactus_item'),


    path('home/banner_shop/', views.BannerShopView.as_view(), name='banner_shop'),
    path('home/banner_shop/<int:banner_id>/', views.BannerShopItemView.as_view(), name='banner_item'),

    path('home/logo/', views.LogoHomeView.as_view(), name='logo'),
    path('home/logo/<int:logo_id>/', views.LogoHomeView.as_view(), name='logo'),
    path('home/seo/', views.SEOHomeView.as_view(), name='seo'),
    path('home/seo/<int:seo_id>/', views.SEOHomeView.as_view(), name='seo'),

    path('newsletter/', views.NewsLetterView.as_view(), name='newsletter'),
    path('newsletter/<int:newsletter_id>/', views.NewsLetterView.as_view(), name='newsletter'),

    path('faq/', views.FAQView.as_view(), name='faq'),
    path('faq/<int:faq_id>/', views.FAQView.as_view(), name='faq_detail'),

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
    path('product/genders/<int:gender_id>/', views.GenderItemView.as_view(), name='gender_item'),
    path('search_product/', views.SearchProductView.as_view({'get': 'list'}), name='search_product'),

    # Product Tag
    path('product/tag/', views.ProductTagListView.as_view(), name='product_list'),
    path('product/tag/<int:product_id>/', views.ProductTagListView.as_view(), name='product_create'),
    path('product/tag/item/<int:product_id>/', views.ProductTagItemView.as_view(), name='product_item'),

    # Add Product Tag
    path('product/addtag/', views.AddProductTagListView.as_view(), name='addtag_post_product'),
    path('product/addtag/<int:product_id>/', views.AddProductTagListView.as_view(), name='addtag_product'),

    # Variant Product
    path('product/variant/', views.VariantPutView.as_view(), name='variant_put'),
    path('product/variant/<int:product_id>/', views.ProductVariantView.as_view(), name='variant_product'),
    path('product/gallery/', views.ProductImageGallery.as_view(), name='image_gallery'),
    path('product/data/<int:product_id>/', views.VariantDataView.as_view(), name='variant_data'),
    path('product/gallery/<int:product_id>/', views.VariantImageView.as_view(), name='gallery_data'),
    path('product/colorimage/<int:product_id>/', views.ColorImageView.as_view(), name='color_image'),

    # orders
    path('order/', views.OrderFilterView.as_view(), name='order_paid'),
    path('order/paid/', views.OrderPaidView.as_view(), name='order_paid'),
    path('order/unpaid/', views.OrderUnpaidView.as_view(), name='order_unpaid'),
    path('order/details/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/customer/<int:order_id>/', views.OrderCustomerView.as_view(), name='order_customer'),
    path('order/items/<int:order_id>/', views.OrderItemsView.as_view(), name='order_items'),
    path('search_order/', views.SearchOrderView.as_view({'get': 'list'}), name='search_order'),

    # Coupon
    path('coupon/', views.CouponView.as_view(), name='coupon'),
    path('coupon/<int:coupon_id>/', views.CouponItemView.as_view(), name='coupon_item'),

    # Backup
    path('manually-backup/', views.ManuallyBackupView.as_view(), name='manually_backup'),

    # Update
    path('manually-update/', views.ManuallyUpdateView.as_view(), name='manually_update'),

    # Shipping
    path('shipping/countries', views.ShippingCountryVIew.as_view(), name='shipping_country'),
    path('shipping/countries/<int:country_id>/', views.ShippingCountryVIew.as_view(), name='put_country'),
    path('shipping/country/<int:country_id>/', views.ShippingVIew.as_view(), name='shipping_item'),
    path('shipping/city/', views.ShippingVIew.as_view(), name='add_city'),
    path('shipping/city/<int:city_id>/', views.ShippingVIew.as_view(), name='put_city'),

    # Pages
    path('pages/about/', views.AboutPageView.as_view(), name='about'),
    path('pages/about/<int:about_id>/', views.AboutPageView.as_view(), name='about'),

    path('pages/contactus/', views.ContactUsPageView.as_view(), name='contactus'),
    path('pages/contactus/<int:contactus_id>/', views.ContactUsPageView.as_view(), name='contactus'),

    path('pages/customerCare/', views.CustomerCarePageView.as_view(), name='customerCare'),
    path('pages/customerCare/<int:customerCare_id>/', views.CustomerCarePageView.as_view(), name='customerCare'),

    path('pages/wholesale/', views.WholesaleInquiryPageView.as_view(), name='wholesale'),
    path('pages/wholesale/<int:wholesale_id>/', views.WholesaleInquiryPageView.as_view(), name='wholesale'),

    path('pages/refund/', views.RefundPolicyPageView.as_view(), name='refund'),
    path('pages/refund/<int:refund_id>/', views.RefundPolicyPageView.as_view(), name='refund'),

    path('pages/sitemapPage/', views.SitemapPageView.as_view(), name='sitemapPage'),
    path('pages/sitemapPage/<int:sitemapPage_id>/', views.SitemapPageView.as_view(), name='sitemapPage'),

    path('pages/career/', views.CareerPageView.as_view(), name='career'),
    path('pages/career/<int:career_id>/', views.CareerPageView.as_view(), name='career'),

    path('pages/shop/', views.ShopPageView.as_view(), name='shop'),
    path('pages/shop/<int:shop_id>/', views.ShopPageView.as_view(), name='shop'),

    path('pages/blog/', views.BlogPageView.as_view(), name='blog'),
    path('pages/blog/<int:blog_id>/', views.BlogPageView.as_view(), name='blog'),

    # Custom Made
    path('product/custom_made/', views.CustomMadeView.as_view(), name='custom_made'),
    path('product/custom_made/<int:custom_id>/', views.CustomMadeItemView.as_view(), name='custom_made_put'),

    path('product/custom_made/CustomerType/', views.CustomerTypeView.as_view(), name='customer_type'),
    path('product/custom_made/CustomerType/<int:customer_type_id>/', views.CustomerTypeItemView.as_view(),
         name='customer_type_put'),

    path('product/custom_made/ProductType/', views.ProductTypeView.as_view(), name='product_type'),
    path('product/custom_made/ProductType/<int:product_type_id>/', views.ProductTypeItemView.as_view(),
         name='product_type_put'),

    path('product/custom_made/BodyArea/', views.BodyAreaView.as_view(), name='body_area'),
    path('product/custom_made/BodyArea/<int:body_area_id>/', views.BodyAreaItemView.as_view(),
         name='body_area_put'),

    path('product/custom_made/ClassNumber/', views.ClassNumberView.as_view()),
    path('product/custom_made/ClassNumber/<int:class_num_id>/', views.ClassNumberItemView.as_view()),

    path('product/custom_made/TreatmentCategory/', views.TreatmentCategoryView.as_view()),
    path('product/custom_made/TreatmentCategory/<int:treatment_category_id>/', views.TreatmentCategoryItemView.as_view()),

    path('product/custom_made/HearAboutUs/', views.HearAboutUsView.as_view()),
    path('product/custom_made/HearAboutUs/<int:hear_about_us_id>/', views.HearAboutUsItemView.as_view()),

    # Compression Class
    path('product/class/', views.CompressionClassView.as_view()),
    path('product/class/<int:class_id>/', views.CompressionClassItemView.as_view()),

    # Side
    path('product/side/', views.SideView.as_view()),
    path('product/side/<int:side_id>/', views.SideItemView.as_view()),

    # Brand
    path('product/brand/', views.BrandView.as_view()),
    path('product/brand/<int:brand_id>/', views.BrandItemView.as_view()),
    path('product/brand/cart/<int:cart_id>/', views.BrandCartDeleteView.as_view()),
    path('product/brand/cart_image/<int:cart_image_id>/', views.BrandCartImageDeleteView.as_view()),

    path('pages/custom_made/', views.CustomMadePageView.as_view(), name='custom_made_page'),
    # path('pages/custom_made/<int:page_id>/', views.CustomMadePageView.as_view(), name='custom_made_page_detail'),

    # path('pages/brand/', views.BrandPageView.as_view(), name='brand_page'),
    # path('pages/brand/<int:brand_id>/', views.BrandPageView.as_view(), name='brand_page_detail'),

    path('custom_made/notif/', views.CustomMadeNotifView.as_view(), name='custom_made_notif'),
    path('contactus/notif/', views.ContactUsNotifView.as_view(), name='contactus_notif'),
]
