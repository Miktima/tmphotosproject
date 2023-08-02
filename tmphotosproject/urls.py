from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings   
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('managephotos/', include('managephotos.urls')),
    path('', include('gallery.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
