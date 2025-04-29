from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('image_slider/', views.ImageSliderView.as_view(), name='image_slider'),
    path('video/', views.VideoHomeView.as_view(), name='video'),
    path('comment/', views.CommentHomeView.as_view(), name='comment'),
    path('content/', views.HomeContentView.as_view(), name='content'),
    path('banner_shop/', views.BannerShopView.as_view(), name='banner_shop'),
    path('logo/', views.LogoHomeView.as_view(), name='logo'),
    path('seo/', views.SEOHomeView.as_view(), name='seo'),
    path('newsletter/', views.NewsLetterView.as_view(), name='newsletter'),
    path('contact_submit/', views.ContactView.as_view(), name='contact_submit'),
    path('telegram_webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('sitemap/', views.SiteMapView.as_view(), name='sitemap'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('contactus/', views.ContactUsPageView.as_view(), name='contactus'),
    path('customerCare/', views.CustomerCarePageView.as_view(), name='customerCare'),
    path('wholesale/', views.WholesaleInquiryPageView.as_view(), name='wholesale'),
    path('refund/', views.RefundPolicyPageView.as_view(), name='refund'),
    path('sitemapPage/', views.SitemapPageView.as_view(), name='sitemapPage'),
    path('career/', views.CareerPageView.as_view(), name='career'),
    path('shop/', views.ShopPageView.as_view(), name='shop'),
    path('blog/', views.BlogPageView.as_view(), name='blog'),
    path('faq/', views.FAQView.as_view(), name='faq'),
]

