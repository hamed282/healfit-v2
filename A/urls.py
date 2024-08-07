from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/v2/admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('api/v2/blog/', include('blog.urls', namespace='blog')),
    path('api/v2/home/', include('home.urls', namespace='home')),
    path('api/v2/product/', include('product.urls', namespace='product')),
    path('api/v2/order/', include('order.urls', namespace='order')),
]
