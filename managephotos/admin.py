from django.contrib import admin
from .models import Genre
from .models import Keywords
from .models import Photo
from .models import Pubstars

admin.site.register(Genre)
admin.site.register(Keywords)
admin.site.register(Photo)
admin.site.register(Pubstars)