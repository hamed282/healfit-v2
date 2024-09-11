from django.contrib.sitemaps import Sitemap
from product.models import ProductModel, Site, ProductCategoryModel, ProductSubCategoryModel
from blog.models import BlogModel
from datetime import datetime


class HomeSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(HomeSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['product:product_all']

    def location(self, item):
        return ''

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ProductWomenSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ProductWomenSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['product:product_list']

    def location(self, item):
        return '/gender/women'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ProductMenSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ProductMenSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['product:product_list']

    def location(self, item):
        return '/gender/men'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ShopSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ShopSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['product:product_all']

    def location(self, item):
        return '/shop'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ProductSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ProductModel.objects.all()

    def lastmod(self, item):
        return item.updated


class ProductCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ProductCategorySitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ProductCategoryModel.objects.all()

    def lastmod(self, item):
        return item.updated


class ProductSubcategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ProductSubcategorySitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ProductSubCategoryModel.objects.all()

    def lastmod(self, item):
        return item.updated


class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(BlogSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return BlogModel.objects.all()

    def lastmod(self, item):
        return item.updated


class BlogAllSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(BlogAllSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['blog:blog_list']

    def location(self, item):
        return '/blog'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class AboutSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(AboutSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/about'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ContactSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ContactSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/contact'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class PrivacySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(PrivacySitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/privacy'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ConditionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ConditionSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/conditions'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ShippingDeliverySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ShippingDeliverySitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/shipping-delivery'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class CustomerCareSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(CustomerCareSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/customer-care'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class WholesaleInquirySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(WholesaleInquirySitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/wholesale-inquiry'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class ReturnRefundSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(ReturnRefundSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/return-refund'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class CareerSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(CareerSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/careers'

    def lastmod(self, item):
        return datetime(2024, 9, 11)


class SitemapSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='healfit.ae', name='healfit.ae')
        return super(SitemapSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['home:seo']

    def location(self, item):
        return '/sitemap'

    def lastmod(self, item):
        return datetime(2024, 9, 11)
