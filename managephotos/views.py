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
		upload_form = UploadImageForm(request.POST, request.FILES)
		if upload_form.is_valid():
			file = request.FILES['file']
			handle_uploaded_file(request.FILES['file'])
			context = {
				"file_name": file.name
			}
			return render(request, 'managephotos/index.html', context)
		else:
			messages.add_message(request, messages.ERROR, upload_form.errors)
			upload_form = UploadImageForm()
			return render(request, 'managephotos/upload_photo.html',\
				{'upload_form': upload_form})
	else:
		upload_form = UploadImageForm()
		return render(request, 'managephotos/upload_photo.html',\
			{'upload_form': upload_form})
	

def handle_uploaded_file(f):
	with open('photo/'+f.name, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


