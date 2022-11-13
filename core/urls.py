import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('store.urls', namespace='store')),
    path('account/', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('basket/', include('basket.urls', namespace='basket')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('orders/', include('orders.urls', namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
