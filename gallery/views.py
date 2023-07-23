from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
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

def image_url(request, url_image):
    # Берем значение записи из таблицы photo 
    # print("image_url: ", url_image)
    photo_instance = get_object_or_404(Photo, url=url_image)
    return HttpResponse(photo_instance.src)

def image_tmb_url(request, url_tmb):
    # Берем значение записи из таблицы photo 
    # print("image_url_min: ", url_tmb)
    photo_instance = get_object_or_404(Photo, url_min=url_tmb)
    return HttpResponse(photo_instance.src_min)

def genre(request, genre):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    # Select photo for genre_id
    reduced_genre = genre.replace("-", " ")
    photo_ins = Photo.objects.order_by("?").filter(genre__genre__iexact=reduced_genre)
    # 9 photos at the page
    paginator = Paginator(photo_ins, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    # print("view.genre:", genre)
    context = {
        "genre": genre_ins,
        "genre_active": genre,
        "page_obj": page_obj
    }
    return render(request, 'gallery/genre.html', context)    

