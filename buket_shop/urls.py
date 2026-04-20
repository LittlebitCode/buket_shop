from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.products.urls')),
    path('orders/', include('apps.orders.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('admin-panel/', include('apps.accounts.admin_urls')),
    path('api/', include('apps.products.api_urls')),
    path('api/orders/', include('apps.orders.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
