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
]
