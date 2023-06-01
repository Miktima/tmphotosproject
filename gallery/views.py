from django.shortcuts import render
from managephotos.models import Genre, Photo
import random

def home(request):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    # Select photo randomly
    random.seed()
    photo_ins = Photo.objects.order_by("pk").all()
    pk_list = []
    weight_list = []
    for ph in photo_ins:
        pk_list.append(ph.pk)
        weight_list.append(ph.star)
    choice_list = random.choices(pk_list, weights=weight_list, k=1)
    photo_ch = Photo.objects.get(pk=choice_list[0])
    context = {
        "genre": genre_ins,
        "rnd_photo": photo_ch 
    }
    return render(request, 'gallery/index.html', context)
