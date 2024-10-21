from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('library.lb_home.urls')),
    path('accounts/', include('library.lb_accounts.urls')),
    path('collections/', include('library.lb_collections.urls')),
    path('events/', include('library.lb_events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
