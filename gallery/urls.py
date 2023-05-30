from django.urls import path, include
from gallery import views

urlpatterns = [
    path('', views.home, name='home'),
]