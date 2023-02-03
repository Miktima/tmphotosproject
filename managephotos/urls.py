from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
		path('add_photo/', views.add_photo, name='add_photo')
]