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
			# Разделяем ключевые слова, очищаем от пробелов и записываем в 
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
	
def edit_photo(request, photo_id):
	genre_list = Genre_en.objects.all()
	star_list = []
	for i in range(1, 6):
		star_list.append(i)
	photo_row = Photo.objects.get(id=photo_id)
	photo_star = photo_row.star
	title_row = Title_en.objects.get(photo__id=photo_id)
	title = title_row.title
	place = title_row.place
	src_row = Src.objects.get(photo__id=photo_id)
	src = src_row.src
	src_min = src_row.src_min
	photo_height = src_row.src_min.height
	photo_width = src_row.src_min.width
	photo_genre_row = list(Photo_genre.objects.filter(photo__id=photo_id).values_list("genre", flat=True))
	photo_keywords_row = Photo_keyword.objects.filter(photo__id=photo_id).\
		values("keyword__id", "keyword__keyword")
	context = {
		"genre_list": genre_list,
		"star_list": star_list,
		"photo_star": photo_star,
		"title": title,
		"place": place,
		"src": src,
		"src_min": src_min,
		"photo_height": photo_height,
		"photo_width": photo_width,
		"photo_genre_row": photo_genre_row,
		"photo_keywords_row": photo_keywords_row,
		"photo_id": photo_id
	}
	return render(request, 'managephotos/edit_photo.html', context=context)

def fixedit_photo(request):
	if request.method == 'POST':
		# Берем из БД значения для проверки их изменения
		photo_id = request.POST["photo_id"]
		photo_row = Photo.objects.get(id=photo_id)
		photo_star = photo_row.star
		title_row = Title_en.objects.get(photo__id=photo_id)
		title = title_row.title
		place = title_row.place
		photo_genre_row = Photo_genre.objects.filter(photo__id=photo_id)
		photo_keywords_row = Photo_keyword.objects.filter(photo__id=photo_id)
		# Проверяем, изменились ли заголовок и/или место, звезды и если изменились, меняем их в БД
		if title != request.POST["photo_title"]:
			Title_en.objects.filter(photo__id=photo_id).update(title=request.POST["photo_title"])
		if place != request.POST["photo_place"]:
			Title_en.objects.filter(photo__id=photo_id).update(title=request.POST["photo_place"])
		if photo_star != int(request.POST["stars"]):
			Photo.objects.filter(id=photo_id).update(star=int(request.POST["stars"]))
		# Проверяем, есть ли ключевые слова на удаление. Если есть, удаляем их из индексной таблицы
		# Если ключевое слово не связано с другими фото, то удаляем его из основной таблицы
		# Примечание: возвращаются в форме только чекнутые чекбоксы
		photo_keywords_row = Photo_keyword.objects.filter(photo__id=photo_id).values_list("keyword__id", flat=True)
		for k in photo_keywords_row:
			index = "kw-" + str(k)
			if index in request.POST:
				Photo_keyword.objects.filter(photo__id=photo_id, keyword__id=k).delete()
				if Photo_keyword.objects.filter(keyword__id=k).count() == 0:
					Keywords_en.objects.filter(id=k).delete()					
		# Проверяем, есть ли добавленные ключевые слова.
		# Если есть, разделяем ключемые слова, очищаем от пробелов и записываем в 
		# таблицу ключевых слов, а потом и в таблицу связей с фото
		# Если такое ключевое слово уже есть, то сразу записываем в 
		# таблицу связей с фото
		keywords = request.POST["add_keywords"]
		if keywords != "":
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
		# Проверяем жанры из формы записаны в индексе БД или нет. Если нет, записываем
		genre_list = Photo_genre.objects.filter(photo__id=photo_id).values_list("genre__id", flat=True)
		for g in request.POST["genre"]:
			if g not in genre_list:
				genre_row = Genre_en.objects.get(id = g)
				ph_genre = Photo_genre(photo=photo_row, genre=genre_row)
				ph_genre.save()
		# Если нет жанра из индекса БД в форме, то удаляем его из индекса
		for gbd in genre_list:
			if gbd not in request.POST["genre"]:
				Photo_genre.objects.filter(photo__id=photo_id, genre__id=gbd).delete()
		return redirect(reverse("index"))
	else:
		messages.add_message(request, messages.ERROR, "Обрабатывается метод POST")
		return redirect(reverse("index"))

def remove_photo(request, photo_id):
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

