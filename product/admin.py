from django.contrib import admin
from .models import (ProductGenderModel, ProductModel, ProductCategoryModel, ProductSubCategoryModel, AddCategoryModel,
                     AddSubCategoryModel)


admin.site.register(ProductGenderModel)
admin.site.register(ProductModel)
admin.site.register(ProductCategoryModel)
admin.site.register(ProductSubCategoryModel)
admin.site.register(AddCategoryModel)
admin.site.register(AddSubCategoryModel)
