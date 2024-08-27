from django.contrib import admin
from .models import (BannerSliderModel, VideoHomeModel, CommentHomeModel, ContentHomeModel, BannerShopModel, LogoModel,
                     SEOHomeModel)


admin.site.register(BannerSliderModel)
admin.site.register(VideoHomeModel)
admin.site.register(CommentHomeModel)
admin.site.register(ContentHomeModel)
admin.site.register(BannerShopModel)
admin.site.register(LogoModel)
admin.site.register(SEOHomeModel)
