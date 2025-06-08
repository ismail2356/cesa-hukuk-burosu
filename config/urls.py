from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('avukatlar/', include('apps.lawyers.urls')),
    path('hizmetler/', include('apps.services.urls')),
    path('blog/', include('apps.blog.urls')),
    path('iletisim/', include('apps.contact.urls')),
]

# Media ve Static dosyalar için URL patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production için media dosyaları
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 