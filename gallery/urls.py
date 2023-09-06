from django.urls import path, re_path, include
from gallery import views

prefix_photo = "DSC"
suffix_tmb = "tn"

urlpatterns = [
    path('', views.home, name='home'),
    path('stocks/', views.stocks, name='stocks'),
    path('<slug:genre>', views.genre, name='genre_menu'),
    path('<slug:genre>/', views.genre, name='genre_content'),
    re_path(r'^(?P<genre>[a-z-]+)/(?P<image>[\w-]+-' + prefix_photo + '_\d{4}[-_\d]{,2}.(html|jpg))$',\
             views.genre_image, name='genre_image'),
    re_path(r'^(?P<url_image>[\w-]+-' + prefix_photo + '_\d{4}[-_\d]{,2}.jpg)$',\
             views.image_url, name='url_image'),
    re_path(r'^(?P<url_tmb>[\w-]+-' + prefix_photo + '_\d{4}[-_\d]{,2}_' + suffix_tmb + \
            '.jpg)$', views.image_tmb_url, name='image_tmb_url'),
]