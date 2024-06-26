from django.db import models
from datetime import date

class Genre(models.Model):
	genre = models.CharField(max_length=50, help_text='Genre of a photo')
	def __str__(self):
		return self.genre
	
class Keywords(models.Model):
	keyword = models.CharField(max_length=70)
	def __str__(self):
		return self.keyword
	
class Photo(models.Model):
	td = date.today()
	upload_path = "photo/" + td.strftime("%Y/%m/%d/")
	src = models.ImageField(upload_to=upload_path)
	url = models.CharField(max_length=100, blank=True)
	src_min = models.ImageField(upload_to=upload_path)
	url_min = models.CharField(max_length=100, blank=True)
	star = models.PositiveSmallIntegerField(default=3)
	genre = models.ManyToManyField(Genre)
	keywords = models.ManyToManyField(Keywords, blank=True)
	title = models.CharField(max_length=200)
	place = models.CharField(max_length=100, blank=True)
	def __str__(self):
		return self.title	

class Pubstars(models.Model):
	ipaddress = models.GenericIPAddressField()
	dtime = models.DateTimeField(auto_now_add=True)
	star = models.PositiveSmallIntegerField()
	photoid = models.PositiveIntegerField()
	def __int__(self):
		return self.photoid	
