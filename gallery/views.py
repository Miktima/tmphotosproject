from django.shortcuts import render

def home(request):
    return render(request, 'gallery/index.html')
