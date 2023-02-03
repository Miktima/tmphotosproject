from django.db import models

class Genre_en(models.Model):
	genre = models.CharField(max_length=50, help_text='Genre of a photo')
	def __str___(self):
		return self.genre
	
class Keywords_en(models.Model):
	keyword = models.CharField(max_length=70)
	def __str___(self):
		return self.keyword

class Title_en(models.Model):
	title = models.CharField(max_length=200)
	place = models.CharField(max_length=100)
	def __str___(self):
		return self.title	
	
class Src(models.Model):
	src = models.CharField(max_length=200, help_text='The path to the photo')
	url = models.URLField(help_text='Friendly URL of the photo')
	src_min = models.CharField(max_length=200, help_text='The path to the thumbnail')
	url_min = models.URLField(help_text='Friendly URL to the thumbnail')

class Photo(models.Model):
	src = models.ForeignKey(Src, on_delete=models.CASCADE)
	star = models.PositiveSmallIntegerField(help_text='The rank (priority) of the photo')
	title = models.ForeignKey(Title_en, on_delete=models.CASCADE)
	genre = models.ForeignKey(Genre_en, on_delete=models.DO_NOTHING)

class Photo_keyword(models.Model):
	photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
	keyword = models.ForeignKey(Keywords_en, on_delete=models.CASCADE)