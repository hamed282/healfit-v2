from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/v2/admin/', include('admin_panel.urls', namespace='admin_panel')),
]
