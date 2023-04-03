from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoForm, KeywordsForm, PhotoEditForm, KeywordsEditForm
from .models import Genre, Photo, Keywords
from django.contrib import messages
from django.urls import reverse
from .MpClass import MpClass
from django.core.paginator import Paginator
import os
from django.contrib.auth.decorators import login_required
@login_required

def index(request):
	photo = Photo.objects.all()
	photo_list = []
	for p in photo:
		photo_list.append([p.id, p.src_min, p.title, p.star])
	paginator = Paginator(photo_list, 3) # Show 3 photos per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)	
	return render(request, 'managephotos/index.html', {'page_obj': page_obj})	

def upload_photo(request):
	photo_form = PhotoForm()
	keywords_form = KeywordsForm()
	context = {
		"photo_form": photo_form,
		"keywords_form": keywords_form
	}
	return render(request, 'managephotos/upload_photo.html', context=context)

def add_photo(request):
	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			# Получаем последнее записанное значение
			photo_row = Photo.objects.last()
			mptool = MpClass()
			# Создаем ЧПУ для фото и эскиза
			f_url = mptool.convertUrl(str(photo_row.src.url), str(photo_row.title))
			f_url_min = mptool.convertUrl(str(photo_row.src_min.url), str(photo_row.title))
			# Обновляем таблицу Photo
			Photo.objects.filter(id=photo_row.pk).update(url=f_url, url_min=f_url_min)
			# Разделяем ключевые слова, очищаем от пробелов и записываем в 
			# таблицу ключевых слов, а потом и в таблицу фото
			# Если такое ключевое слово уже есть, то сразу записываем в 
			# таблицу с фото
			form_keywords = KeywordsForm(request.POST)
			if form_keywords.is_valid():
				keywords = form_keywords.cleaned_data["keywords_bulk"]
				keywords_list = keywords.split(",")
				photo_row = Photo.objects.last()
				for kword in keywords_list:
					kw = kword.strip()
					kw_obj, created = Keywords.objects.get_or_create(keyword = kw)
					photo_row.keywords.add(kw_obj)
					photo_row.save()
				return redirect(reverse("index"))
			else:
				messages.add_message(request, messages.ERROR, form_keywords.errors)
				photo_form = PhotoForm()
				keywords_form = KeywordsForm()
				context = {
					"photo_form": photo_form,
					"keywords_form": keywords_form
				}				
				return render(request, 'managephotos/upload_photo.html', context)
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			photo_form = PhotoForm()
			keywords_form = KeywordsForm()
			context = {
				"photo_form": photo_form,
				"keywords_form": keywords_form
			}				
			return render(request, 'managephotos/upload_photo.html', context)
	else:
		photo_form = PhotoForm()
		keywords_form = KeywordsForm()
		context = {
			"photo_form": photo_form,
			"keywords_form": keywords_form
		}				
		return render(request, 'managephotos/upload_photo.html', context)

	
def edit_photo(request, photo_id):
	photo_instance = get_object_or_404(Photo, pk=photo_id)
	if request.method == 'POST':
		form = PhotoEditForm(request.POST, request.FILES, instance=photo_instance)
		if form.is_valid():
			form.save()
			form_keywords = KeywordsEditForm(request.POST)
			if form_keywords.is_valid():
				keywords = form_keywords.cleaned_data["keywords_bulk"]
				if keywords != "":
					keywords_list = keywords.split(",")
					photo_row = Photo.objects.last()
					for kword in keywords_list:
						kw = kword.strip()
						kw_obj, created = Keywords.objects.get_or_create(keyword = kw)
						photo_row.keywords.add(kw_obj)
						photo_row.save()
				return redirect(reverse("index"))
			else:
				messages.add_message(request, messages.ERROR, form_keywords.errors)
				photoedit_form = PhotoEditForm(instance=photo_instance)
				keywords_form = KeywordsEditForm()
				context = {
					"photoedit_form": photoedit_form,
					"keywords_form": keywords_form,
					"photo": photo_instance,
				}				
				return render(request, 'managephotos/edit_photo.html', context)
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			photoedit_form = PhotoEditForm(instance=photo_instance)
			keywords_form = KeywordsEditForm()
			context = {
				"photoedit_form": photoedit_form,
				"keywords_form": keywords_form,
				"photo": photo_instance,
			}				
			return render(request, 'managephotos/edit_photo.html', context)
	else:
		photoedit_form = PhotoEditForm(instance=photo_instance)
		keywords_form = KeywordsEditForm()
		context = {
			"photo": photo_instance,
			"photoedit_form": photoedit_form,
			"keywords_form": keywords_form
		}
		return render(request, 'managephotos/edit_photo.html', context=context)

def remove_photo(request, photo_id):
	# Берем значение записи из таблицы photo 
	photo_instance = get_object_or_404(Photo, pk=photo_id)
	# Удаляем файлы 
	os.remove(photo_instance.src.path)
	os.remove(photo_instance.src_min.path)
	# и удаляем запись
	photo_instance.delete()
	return redirect(reverse("index"))

