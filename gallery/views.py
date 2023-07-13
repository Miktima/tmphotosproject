from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
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

def image_url(request, url):
    # Берем значение записи из таблицы photo 
    print("image_url: ", url)
    photo_instance = get_object_or_404(Photo, url=url)
    return HttpResponse(photo_instance.src)

def image_tmb_url(request, url):
    # Берем значение записи из таблицы photo 
    print("image_url_min: ", url)
    photo_instance = get_object_or_404(Photo, url_min=url)
    return HttpResponse(photo_instance.src_min)

def genre(request, genre):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    # Select photo for genre_id
    photo_ins = Photo.objects.order_by("pk").filter(genre__genre__iexact=genre)
    print("view.genre:", genre)
    context = {
        "genre": genre_ins,
        "genre_active": genre,
        "photo": photo_ins 
    }
    return render(request, 'gallery/genre.html', context)    

