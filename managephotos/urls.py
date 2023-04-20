from django.urls import path, include
from managephotos import views

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='index'),
		path('add_photo/', views.add_photo, name='add_photo'),
		path('edit_photo/<int:photo_id>/', views.edit_photo, name='edit_photo'),
    path('remove_photo/<int:photo_id>/', views.remove_photo, name='remove_photo'),
    path('accounts/', include('django.contrib.auth.urls')),
]