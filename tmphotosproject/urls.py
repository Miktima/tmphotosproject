from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings   
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from .sitemap import PhotoSitemap, StaticSitemap

sitemaps = {
    "genre": PhotoSitemap,
    "statc": StaticSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('managephotos/', include('managephotos.urls')),
    path('', include('gallery.urls')),
    path('sitemap.xml', sitemap,  {'sitemaps': sitemaps}, 
        name='django.contrib.sitemaps.views.sitemap',)
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

handler404 = 'gallery.views.error404'