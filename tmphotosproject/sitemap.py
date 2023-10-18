from django.contrib.sitemaps import Sitemap
from managephotos.models import Genre, Photo
from django.urls import reverse

class PhotoSitemap(Sitemap):
    def items(self):
        return Genre.objects.order_by("pk").all()
    
    def location(self, item):
        return item.replace(" ", "-").lower()
