from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('managephotos/', include('managephotos.urls')),
    path('admin/', admin.site.urls),
]

