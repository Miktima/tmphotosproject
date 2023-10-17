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
    # Return 10 photos or less
    nphotos = 10 if len(pk_list) > 10 else len(pk_list)
    choice_list = []
    # Get unrepeated list of photos
    for i in range (nphotos):
        cl = random.choices(pk_list, weights=weight_list, k=1)
        choice_list.append(cl[0])
        # remove chosen elements
        pos = pk_list.index(cl[0])
        pk_list.remove(cl[0])
        weight_list.pop(pos)
    # photo_ch = Photo.objects.get(pk=choice_list[0])
    photoObj = []
    i = 0
    for u in choice_list:
        photo_ch = Photo.objects.get(pk=u)        
        tmpDict = {}
        tmpDict["url"] = photo_ch.url
        if i == 0:
            tmpDict["active"] = 1
            i += 1
        else:
            tmpDict["active"] = 0
        tmpDict["url_min"] = photo_ch.url_min
        tmpDict["title"] = photo_ch.title
        tmpDict["place"] = photo_ch.place
        tmpDict["keywords"] = photo_ch.keywords.all()
        photoObj.append(tmpDict)
    context = {
        "genre": genre_ins,
        "rnd_photo": photoObj
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
    # fill dict with new urls
    photoObj = []
    for u in photo_ins:        
        tmpDict = {}
        tmpDict["url"] = (u.url).replace(".jpg", ".html")
        tmpDict["url_min"] = u.url_min
        tmpDict["title"] = u.title
        photoObj.append(tmpDict)
    # 9 photos at the page
    # paginator = Paginator(photo_ins, 9)
    paginator = Paginator(photoObj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    # print("view.genre:", genre)
    context = {
        "genre": genre_ins,
        "genre_active": genre,
        "page_obj": page_obj
    }
    return render(request, 'gallery/genre.html', context)    

def genre_image(request, genre, image):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    # Change from html to jpg suffix, if html suffix occurs
    if ".html" in image:
        image = image.replace(".html", ".jpg")

    # fill dict with new urls of hires photos for Carousel
    photoObj = []
    # select choosen photo
    photo_instance = get_object_or_404(Photo, url=image)
    tmpDict = {}
    tmpDict["url"] = photo_instance.url
    tmpDict["active"] = 1
    tmpDict["url_min"] = photo_instance.url_min
    tmpDict["title"] = photo_instance.title
    tmpDict["place"] = photo_instance.place
    tmpDict["keywords"] = photo_instance.keywords.all()
    photoObj.append(tmpDict)
    # Select 9 random photo for genre_id
    reduced_genre = genre.replace("-", " ")
    photo_ins = Photo.objects.order_by("?").filter(genre__genre__iexact=reduced_genre)

    i = 0
    for u in photo_ins:
        if i >= 9:
            break        
        if u.url != image:
            tmpDict = {}
            tmpDict["url"] = u.url
            tmpDict["active"] = 0
            tmpDict["url_min"] = u.url_min
            tmpDict["title"] = u.title
            tmpDict["place"] = u.place
            tmpDict["keywords"] = u.keywords.all()
            photoObj.append(tmpDict)
            i += 1
    context = {
        "genre": genre_ins,
        "genre_active": genre,
        # "photo": photo_instance,
        "photo_list": photoObj
    }
    return render(request, 'gallery/genre_image.html', context)    

def stocks(request):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    context = {
        "genre": genre_ins,
    }
    return render(request, 'gallery/stocks.html', context)

def error404(request, exception):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    context = {
        "genre": genre_ins,
    }
    response = render(request, 'gallery/404.html', context)
    response.status_code = 404
    return response
