from django.contrib.sitemaps import Sitemap
from managephotos.models import Genre, Photo
from django.urls import reverse

class PhotoSitemap(Sitemap):
    protocol = 'https'
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Genre.objects.order_by("pk").all()
    
    def location(self, item):
        return '/%s' % item.genre.replace(" ", "-").lower()

class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return ['home', 'stocks']

    def location(self, item):
        return reverse(item)