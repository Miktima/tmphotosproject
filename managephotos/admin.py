from django.contrib import admin
from .models import Genre
from .models import Keywords
from .models import Photo

admin.site.register(Genre)
admin.site.register(Keywords)
admin.site.register(Photo)
