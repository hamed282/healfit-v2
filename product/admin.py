from django.contrib import admin
from .models import (ProductCategoryModel, ProductModel, PopularProductModel, SizeProductModel, ProductVariantModel,
                     ColorProductModel, ProductSubCategoryModel, AddSubCategoryModel, AddCategoryModel,
                     ProductGenderModel, AddImageGalleryModel, ExtraGroupModel, ProductTagModel, AddProductTagModel,
                     FavUserModel, CouponModel, ProductCouponModel, CompressionClassModel, SideModel, ProductBrandModel,
                     CustomMadeModel, TreatmentCategoryModel, ProductTypeModel, BodyAreaModel, ClassNumberModel,
                     CustomerTypeModel, HearAboutUsModel, CustomMadePageModel, CustomerTestimonialsModel,
                     BrandPageModel, BrandCartModel, BrandCartImageModel)
from django.utils.html import format_html


class ProductGenderAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


class CategoryInline(admin.TabularInline):
    model = AddCategoryModel
    extra = 1


class SubCategoryInline(admin.TabularInline):
    model = AddSubCategoryModel
    extra = 1


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'priority']
    # readonly_fields = ["slug"]
    inlines = (CategoryInline, )


class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory', 'priority']
    # readonly_fields = ["slug"]
    inlines = (SubCategoryInline, )


class ProductImageGalleryAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        else:
            return "No Image Available"
    list_display = ['product', 'color', 'image_tag']


class ImageGalleryInline(admin.TabularInline):
    model = AddImageGalleryModel
    extra = 1


class TagInline(admin.TabularInline):
    model = AddProductTagModel
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'priority', 'brand']
    inlines = (ImageGalleryInline, CategoryInline, SubCategoryInline, TagInline)


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'size', 'quantity', 'price', 'percent_discount', 'compression_class',
                    'side']
    readonly_fields = ["slug"]


class SizeProductAdmin(admin.ModelAdmin):
    list_display = ['size', 'priority']


class CategoryTagAdmin(admin.ModelAdmin):
    list_display = ['tag']


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['tag']


class FavUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']


class CouponInline(admin.TabularInline):
    model = ProductCouponModel
    extra = 1


class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'coupon_code', 'discount_percent', 'discount_amount', 'active', 'infinite']
    inlines = (CouponInline,)


class BrandCartImageInline(admin.TabularInline):
    model = BrandCartImageModel
    extra = 1
    fields = ['image', 'image_alt', 'priority']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        else:
            return "No Image Available"
    image_tag.short_description = 'Preview'


class BrandCartAdmin(admin.ModelAdmin):
    list_display = ['brand', 'content']
    inlines = [BrandCartImageInline]


admin.site.register(ProductCategoryModel, ProductCategoryAdmin)
admin.site.register(ProductGenderModel, ProductGenderAdmin)
admin.site.register(ProductSubCategoryModel, ProductSubCategoryAdmin)
admin.site.register(AddImageGalleryModel, ProductImageGalleryAdmin)
admin.site.register(PopularProductModel)
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(SizeProductModel, SizeProductAdmin)
admin.site.register(ProductVariantModel, ProductVariantAdmin)
admin.site.register(ColorProductModel)
admin.site.register(AddCategoryModel)
admin.site.register(AddSubCategoryModel)
admin.site.register(CompressionClassModel)
admin.site.register(SideModel)
admin.site.register(ExtraGroupModel)
admin.site.register(CustomMadeModel)
admin.site.register(HearAboutUsModel)
admin.site.register(ProductTypeModel)
admin.site.register(ClassNumberModel)
admin.site.register(TreatmentCategoryModel)
admin.site.register(CustomerTypeModel)
admin.site.register(BodyAreaModel)
admin.site.register(ProductTagModel, ProductTagAdmin)
admin.site.register(AddProductTagModel)
admin.site.register(ProductBrandModel)
admin.site.register(CustomMadePageModel)
admin.site.register(CustomerTestimonialsModel)
admin.site.register(BrandPageModel)
admin.site.register(BrandCartModel, BrandCartAdmin)
admin.site.register(BrandCartImageModel)
admin.site.register(FavUserModel, FavUserAdmin)
admin.site.register(CouponModel, CouponAdmin)
