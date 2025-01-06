from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from sitemaps import (ProductWomenSitemap, ProductMenSitemap, ProductSitemap, ProductCategorySitemap,
                      ProductSubcategorySitemap, ShopSitemap, HomeSitemap, BlogSitemap, BlogAllSitemap, AboutSitemap,
                      ContactSitemap, PrivacySitemap, ShippingDeliverySitemap, ConditionSitemap, SitemapSitemap,
                      CareerSitemap, ReturnRefundSitemap, CustomerCareSitemap, WholesaleInquirySitemap)


sitemaps = {
    'home': HomeSitemap,
    'women': ProductWomenSitemap,
    'men': ProductMenSitemap,
    'shop': ShopSitemap,
    'product': ProductSitemap,
    'product_category': ProductCategorySitemap,
    'product_subcategory': ProductSubcategorySitemap,
    'blog': BlogSitemap,
    'blog_all': BlogAllSitemap,
    'about': AboutSitemap,
    'contact': ContactSitemap,
    'privacy': PrivacySitemap,
    'shipping': ShippingDeliverySitemap,
    'condition': ConditionSitemap,
    'sitemap': SitemapSitemap,
    'careers': CareerSitemap,
    'return_refund': ReturnRefundSitemap,
    'customer_care': CustomerCareSitemap,
    'wholesale': WholesaleInquirySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/accounts/', include('accounts.urls', namespace='accounts')),
    path(r'api/v2/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/v2/admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('api/v2/blog/', include('blog.urls', namespace='blog')),
    path('api/v2/home/', include('home.urls', namespace='home')),
    path('api/v2/product/', include('product.urls', namespace='product')),
    path('api/v2/order/', include('order.urls', namespace='order')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

]
