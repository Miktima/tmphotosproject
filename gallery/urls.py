from django.urls import path, include
from gallery import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:url>', views.image_url, name='image_url'),
    path('<str:url>', views.image_tmb_url, name='image_tmb_url'),
    path('<str:genre>', views.genre, name='genre')
]