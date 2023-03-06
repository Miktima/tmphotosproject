from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
		path('add_photo/', views.add_photo, name='add_photo'),
		path('edit_photo/<int:photo_id>/', views.edit_photo, name='edit_photo'),
    path('remove_photo/<int:photo_id>/', views.remove_photo, name='remove_photo'),
    path('fixedit_photo/', views.fixedit_photo, name='fixedit_photo'),
    path('accounts/', include('django.contrib.auth.urls')),
]