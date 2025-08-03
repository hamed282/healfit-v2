from django.contrib import admin
from .models import (BannerSliderModel, VideoHomeModel, CommentHomeModel, BannerShopModel, LogoModel,
                     SEOHomeModel, NewsLetterModel, ContactSubmitModel, TelegramBotModel, AboutPageModel,
                     CareerPageModel, SitemapPageModel, CustomerCarePageModel, BlogPageModel, ShopPageModel,
                     RefundPolicyPageModel, ContactUsPageModel, WholesaleInquiryPageModel, BannerSliderMobileModel,
                     Content1Model, Content2Model, Content3Model, FAQModel, PrivacyPolicyPageModel,
                     TermConditionPageModel, ShippingDeliveryPageModel)


class BannerSliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority']


class BannerSliderMobileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority']


admin.site.register(BannerSliderModel, BannerSliderAdmin)
admin.site.register(BannerSliderMobileModel, BannerSliderMobileAdmin)
admin.site.register(VideoHomeModel)
admin.site.register(CommentHomeModel)
admin.site.register(Content1Model)
admin.site.register(Content2Model)
admin.site.register(Content3Model)
admin.site.register(BannerShopModel)
admin.site.register(LogoModel)
admin.site.register(SEOHomeModel)
admin.site.register(NewsLetterModel)
admin.site.register(ContactSubmitModel)
admin.site.register(TelegramBotModel)
admin.site.register(CareerPageModel)
admin.site.register(PrivacyPolicyPageModel)
admin.site.register(TermConditionPageModel)
admin.site.register(ShippingDeliveryPageModel)
admin.site.register(RefundPolicyPageModel)
admin.site.register(ContactUsPageModel)
admin.site.register(SitemapPageModel)
admin.site.register(CustomerCarePageModel)
admin.site.register(BlogPageModel)
admin.site.register(ShopPageModel)
admin.site.register(WholesaleInquiryPageModel)
admin.site.register(AboutPageModel)
admin.site.register(FAQModel)
