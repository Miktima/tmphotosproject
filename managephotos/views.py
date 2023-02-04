from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadImageForm
from .models import Genre_en, Photo
from django.contrib import messages

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
	return render(request, 'managephotos/upload_photo.html', {'upload_form': upload_form})

def add_photo(request):
	if request.method == 'POST':
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return render(request, 'managephotos/index.html')
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			upload_form = UploadImageForm()
			return render(request, 'managephotos/upload_photo.html',\
				{'upload_form': upload_form})
	else:
		upload_form = UploadImageForm()
		return render(request, 'managephotos/upload_photo.html',\
			{'upload_form': upload_form})
	



