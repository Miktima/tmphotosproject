from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UploadImageForm
from .models import Genre_en, Photo, Title_en, Src, Keywords_en, Photo_keyword, Photo_genre
from django.contrib import messages
from django.urls import reverse
from .MpClass import MpClass

def index(request):
	photo = Photo.objects.all()
	photo_list = []
	for p in photo:
		image_src = Src.objects.get(id=p.src.id)
		url = image_src.src_min
		star = p.star
		photo_list.append([p.id, url, p.title.title, star])
	context = {
		"photo_list": photo_list,
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
			src_row = Src.objects.last()
			title = request.POST["photo_title"]
			# Записываем заголовок и место (если есть) в базу данных
			title_row = Title_en(title = title, place = request.POST["photo_place"])
			title_row.save()
			star = request.POST["stars"]
			# Записываем сведения по фото в БД
			photo_row = Photo(src = src_row, title = title_row, star = int(star))
			photo_row.save()
			mptool = MpClass()
			# Создаем ЧПУ для фото и эскиза
			f_url = mptool.convertUrl(str(src_row.src), title)
			f_url_min = mptool.convertUrl(str(src_row.src_min), title)
			# Обновляем таблицу SRC
			src_row.url = f_url
			src_row.url_min = f_url_min
			src_row.save()
			# Разделяем ключемые слова, очищаем от пробелов и записываем в 
			# таблицу ключевых слов, а потом и в таблицу связей с фото
			# Если такое ключевое слово уже есть, то сразу записываем в 
			# таблицу связей с фото
			keywords = request.POST["keywords"]
			keywords_list = keywords.split(",")
			for kword in keywords_list:
				kw = kword.strip()
				kw_exist = Keywords_en.objects.filter(keyword = kw)
				if kw_exist.exists():
					kw_link = Photo_keyword(photo=photo_row, keyword=kw_exist)
				else:
					keywords_row = Keywords_en(keyword = kw)
					keywords_row.save()
					kw_link = Photo_keyword(photo=photo_row, keyword=keywords_row)
				kw_link.save()
			for g in request.POST["genre"]:
				genre_row = Genre_en.objects.get(id = g)
				ph_genre = Photo_genre(photo=photo_row, genre=genre_row)
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
	



