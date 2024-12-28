from django.contrib import admin
from .models import (BannerSliderModel, VideoHomeModel, CommentHomeModel, ContentHomeModel, BannerShopModel, LogoModel,
                     SEOHomeModel, NewsLetterModel, ContactSubmitModel, TelegramBotModel, AboutPageModel,
                     CareerPageModel, SitemapPageModel, CustomerCarePageModel, BlogPageModel, ShopPageModel,
                     RefundPolicyPageModel, ContactUsPageModel, WholesaleInquiryPageModel)


class BannerSLiderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority']


admin.site.register(BannerSliderModel)
admin.site.register(VideoHomeModel)
admin.site.register(CommentHomeModel)
admin.site.register(ContentHomeModel)
admin.site.register(BannerShopModel)
admin.site.register(LogoModel)
admin.site.register(SEOHomeModel)
admin.site.register(NewsLetterModel)
admin.site.register(ContactSubmitModel)
admin.site.register(TelegramBotModel)
admin.site.register(CareerPageModel)
admin.site.register(RefundPolicyPageModel)
admin.site.register(ContactUsPageModel)
admin.site.register(SitemapPageModel)
admin.site.register(CustomerCarePageModel)
admin.site.register(BlogPageModel)
admin.site.register(ShopPageModel)
admin.site.register(WholesaleInquiryPageModel)
admin.site.register(AboutPageModel)
