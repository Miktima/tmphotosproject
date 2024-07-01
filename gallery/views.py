from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.urls import reverse
from managephotos.models import Genre, Photo, Pubstars
from django.db.models import Avg
import random
import math

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
        # Среднее по публичному голосованию, если результатов нет, то возвращаем, то, что присвоено фотографии
        avgPubstars = Pubstars.objects.filter(photoid=u).aggregate(Avg("star", default=photo_ch.star))
        avgStars = (avgPubstars['star__avg'] + photo_ch.star)/2
        # mask for stars: 1 - fill star, 0 - half star, -1 - empty star
        # starmask = photo_ch.star * [1] + (5 - photo_ch.star) * [-1]
        starmask = math.floor(avgStars) * [1] + \
            (math.ceil(avgStars) - math.floor(avgStars)) * [0] + \
            (5 - math.ceil(avgStars)) * [-1]
        tmpDict["url_min"] = photo_ch.url_min
        tmpDict["title"] = photo_ch.title
        tmpDict["place"] = photo_ch.place
        tmpDict["stars"] = starmask
        tmpDict["photoid"] = u
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
    try:
        genre_instance = Genre.objects.get(genre=reduced_genre)
    except Genre.DoesNotExist:
        raise Http404("No Genre matches!")
    photo_ins = Photo.objects.order_by("-pk").filter(genre__genre__iexact=reduced_genre)
    # fill dict with new urls
    photoObj = []
    for u in photo_ins:        
        tmpDict = {}
        tmpDict["url"] = (u.url).replace(".jpg", ".html")
        tmpDict["url_min"] = u.url_min
        tmpDict["title"] = u.title
        photoObj.append(tmpDict)
    # 9 photos at the page
    paginator = Paginator(photoObj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # print("view.genre:", genre)
    context = {
        "genre": genre_ins,
        "genre_active": genre,
        "page_obj": page_obj,
    }
    return render(request, 'gallery/genre.html', context)    

def genre_image_old(request, genre, image): #OBSOLETE
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

def genre_image(request, genre, image):
    # Select genres
    genre_ins = Genre.objects.order_by("pk").all()
    # Change from html to jpg suffix, if html suffix occurs
    if ".html" in image:
        image = image.replace(".html", ".jpg")

    # select choosen photo
    photo_instance = get_object_or_404(Photo, url=image)
    photoDict = {}
    photoDict["url"] = photo_instance.url
    photoDict["url_min"] = photo_instance.url_min
    photoDict["title"] = photo_instance.title
    photoDict["place"] = photo_instance.place
    photoDict["photoid"] = photo_instance.pk
    photoDict["keywords"] = photo_instance.keywords.all()
    # Среднее по публичному голосованию, если результатов нет, то возвращаем, то, что присвоено фотографии
    avgPubstars = Pubstars.objects.filter(photoid=photo_instance.pk).aggregate(Avg("star", default=photo_instance.star))
    print ("Stars (pub + own):", avgPubstars['star__avg'], photo_instance.star)
    avgStars = (avgPubstars['star__avg'] + photo_instance.star)/2
    # mask for stars: 1 - fill star, 0 - half star, -1 - empty star
    starmask = math.floor(avgStars) * [1] + \
            (math.ceil(avgStars) - math.floor(avgStars)) * [0] + \
            (5 - math.ceil(avgStars)) * [-1]
    photoDict["stars"] = starmask

    context = {
        "genre": genre_ins,
        "genre_active": genre,
        # "photo": photo_instance,
        "photo": photoDict
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

def save_star(request):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')      
        phandst = (request.POST['star']).split("__")
        pubstar = Pubstars()
        pubstar.ipaddress = ip
        pubstar.star = int(phandst[1])
        pubstar.photoid = int(phandst[0])
        pubstar.save()
        return HttpResponse("OK")
    else:
        return render(request, 'gallery/index.html')
