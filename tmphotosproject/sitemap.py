from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from managephotos.models import Genre, Photo
from django.urls import reverse
import datetime

class PhotoSitemap(Sitemap):
    protocol = 'https'
    priority = 0.5
    changefreq = "weekly"

    def items(self):
      return Photo.objects.all()
    
    def location(self, item):
      # genre for menu
      genre_ins = item.genre.first()
      genre = genre_ins.genre.replace(" ", "-").lower()
      # photo friendly url
      photo = (item.url).replace(".jpg", ".html")
      return '/%s/%s' % (genre, photo)
    
    def lastmod(self, item):
      # Get date from src of the uploaded file: upload_path = "photo/" + td.strftime("%Y/%m/%d/")
      src = (item.src.path).split("/")
      i = len(src)
      # Date from path /Y/m/d/name_of_file
      photo_date = datetime.date(int(src[i-4]), int(src[i-3]), int(src[i-2]))
      return photo_date

    def __get(self, name, obj, default=None):
      try:
        attr = getattr(self, name)
      except AttributeError:
        return default
      if callable(attr):
        return attr(obj)
      return attr

    def get_image (self, item):
      # For common purpose get_image return list of urls
      url = []
      url.append(item.url)
      return url

    def get_urls(self, page=1, site=None, protocol=None):
      # Determine protocol
      if self.protocol is not None:
        protocol = self.protocol
      if protocol is None:
        protocol = 'http'

      # Determine domain
      if site is None:
        if Site._meta.installed:
            try:
                site = Site.objects.get_current()
            except Site.DoesNotExist:
                pass
        if site is None:
            raise ImproperlyConfigured("To use sitemaps, either enable the sites framework or pass a Site/RequestSite object in your view.")
      domain = site.domain

      urls = []
      for item in self.paginator.page(page).object_list:
        loc = "%s://%s%s" % (protocol, domain, self.__get('location', item))
        priority = self.__get('priority', item, None)
        url_info = {
            'item':       item,
            'location':   loc,
            'lastmod':    self.__get('lastmod', item, None),
            'changefreq': self.__get('changefreq', item, None),
            'priority':   str(priority is not None and priority or ''),
            'images'   :  self.get_image(item)
        }
        urls.append(url_info)
      return urls
    

class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return ['home', 'stocks']

    def location(self, item):
        return reverse(item)
    
    # def lastmod(self, item):
    #   if item == "stocks":
    #       delta = datetime.timedelta (days = 365)
    #   else:
    #       delta = datetime.timedelta (days = 14)
    #   return datetime.date.today() - delta
