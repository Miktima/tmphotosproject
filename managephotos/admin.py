from django.contrib import admin
from .models import Genre_en
from .models import Keywords_en
from .models import Title_en
from .models import Src
from .models import Photo
from .models import Photo_keyword, Photo_genre

admin.site.register(Genre_en)
admin.site.register(Keywords_en)
admin.site.register(Title_en)
admin.site.register(Src)
admin.site.register(Photo)
admin.site.register(Photo_keyword)
admin.site.register(Photo_genre)
