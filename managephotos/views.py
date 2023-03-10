from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import PhotoForm, KeywordsForm, PhotoEditForm
from .models import Genre, Photo, Keywords
from django.contrib import messages
from django.urls import reverse
from .MpClass import MpClass
import os
from django.contrib.auth.decorators import login_required
@login_required

def index(request):
	photo = Photo.objects.all()
	photo_list = []
	for p in photo:
		photo_list.append([p.id, p.src_min, p.title, p.star])
	context = {
		"photo_list": photo_list,
	}
	return render(request, 'managephotos/index.html', context)	

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
				keywords = form_keywords.cleaned_data["keywords"]
				keywords_list = keywords.split(",")
				photo_row = Photo.objects.last()
				for kword in keywords_list:
					kw = kword.strip()
					kw_exist = Keywords.objects.filter(keyword = kw)
					if kw_exist.exists() == False:
						photo_row.keywords.add(kw_exist)
					else:
						keywords_row = Keywords(keyword = kw)
						keywords_row.save()
						photo_row.keywords.add(keywords_row)
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
	photoedit_form = PhotoEditForm(instance=photo_instance)
	keywords_form = KeywordsForm()
	context = {
		"photoedit_form": photoedit_form,
		"keywords_form": keywords_form
	}
	return render(request, 'managephotos/edit_photo.html', context=context)

def fixedit_photo(request, photo_id):
	photo_instance = get_object_or_404(Photo, pk=photo_id)
	if request.method == 'POST':
		form = PhotoEditForm(request.POST, request.FILES, instance=photo_instance)
		if form.is_valid():
			form.save()
			form_keywords = KeywordsForm(request.POST)
			if form_keywords.is_valid():
				keywords = form_keywords.cleaned_data["keywords"]
				if keywords != "":
					keywords_list = keywords.split(",")
					photo_row = Photo.objects.last()
					for kword in keywords_list:
						kw = kword.strip()
						kw_exist = Keywords.objects.filter(keyword = kw)
						if kw_exist.exists() == False:
							photo_row.keywords.add(kw_exist)
						else:
							keywords_row = Keywords(keyword = kw)
							keywords_row.save()
							photo_row.keywords.add(keywords_row)
						photo_row.save()
					return redirect(reverse("index"))
			else:
				messages.add_message(request, messages.ERROR, form_keywords.errors)
				photo_form = PhotoEditForm(instance=photo_instance)
				keywords_form = KeywordsForm()
				context = {
					"photo_form": photo_form,
					"keywords_form": keywords_form
				}				
				return render(request, 'managephotos/edit_photo.html', context)
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			photo_form = PhotoEditForm(instance=photo_instance)
			keywords_form = KeywordsForm()
			context = {
				"photo_form": photo_form,
				"keywords_form": keywords_form
			}				
			return render(request, 'managephotos/edit_photo.html', context)
	else:
		photo_form = PhotoForm()
		keywords_form = KeywordsForm()
		context = {
			"photo_form": photo_form,
			"keywords_form": keywords_form
		}				
		return render(request, 'managephotos/edit_photo.html', context)

def remove_photo(request, photo_id):
	# Берем значение записи из таблицы photo 
	photo_instance = get_object_or_404(Photo, pk=photo_id)
	# Удаляем файлы 
	os.remove(photo_instance.src.path)
	os.remove(photo_instance.src_min.path)
	# и удаляем запись
	photo_instance.delete()
	return redirect(reverse("index"))

