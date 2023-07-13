from django.urls import path, re_path, include
from gallery import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'([a-zA-Z\s]+)', views.genre, name='genre'),
    re_path(r'(\w+)DSC_(\d+).jpg$', views.image_url, name='image_url'),
    re_path(r'(\w+DSC_(\d)+_(\w)+).jpg$', views.image_tmb_url, name='image_tmb_url'),
]