from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UploadImageForm
from .models import Genre_en, Photo, Title_en, Src, Keywords_en, Photo_keyword, Photo_genre
from django.contrib import messages
from django.urls import reverse
from MpClass import MpClass

def index(request):
	list_photo = Photo.objects.all()
	photo_title_list = []
	for photo in list_photo:
		photo_title_list.append(photo.title)
	context = {
		"photo_list": photo_title_list,
	}
	return render(request, 'managephotos/index.html', context)	

def upload_photo(request):
	upload_form = UploadImageForm()
	genre_list = Genre_en.objects.all()
	star_list = []
	for i in range(1, 6):
		star_list.append(i)
	context = {
		'upload_form': upload_form,
		"genre_list": genre_list,
		"star_list": star_list
	}
	return render(request, 'managephotos/upload_photo.html', context=context)

def add_photo(request):
	if request.method == 'POST':
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			title_row = Title_en(title = request.POST["photo_title"],\
				place = request.POST["photo_place"])
			title_row.save()
			src_row = Src.objects.last()
			star = request.POST["stars"]
			photo_row = Photo(src = src_row.id, title = title_row.id, star = int(star))
			photo_row.save()
			id_photo = photo_row.id
			f_url = MpClass.convertUrl(src_row.src, request.POST["photo_title"])
			f_url_min = MpClass.convertUrl(src_row.src_min, request.POST["photo_title"])
			src_row.url = f_url
			src_row.url_min = f_url_min
			src_row.save()
			keywords = request.POST["photo_title"]
			keywords_list = keywords.split(",")
			for kword in keywords_list:
				kw = kword.strip()
				kw_exist = Keywords_en.objects.filter(keyword = kw)
				if not kw_exist:
					keywords_row = Keywords_en(keyword=kw)
					id_kw = keywords_row.id
				else:
					id_kw = kw_exist.id
				kw_link = Photo_keyword(photo=id_photo, keyword=id_kw)
				kw_link.save()
			for g in request.POST["genre"]:
				ph_genre = Photo_genre(photo=id_photo, genre=g)
				ph_genre.save()
			return redirect(reverse("index"))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			upload_form = UploadImageForm()
			return render(request, 'managephotos/upload_photo.html',\
				{'upload_form': upload_form})
	else:
		upload_form = UploadImageForm()
		return render(request, 'managephotos/upload_photo.html',\
			{'upload_form': upload_form})
	



