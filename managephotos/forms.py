from django import forms
from .models import Photo, Keywords
import re


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ["src", "src_min", "star", "genre", "title", "place"]
		CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),]
		labels = {
			'src': 'The path to the hires photo',
			'src_min': 'The path to the thumbnail',
			"star": 'The rank (priority) of the photo'
		}
		widgets = {
			'star': forms.RadioSelect(choices=CHOICES),
		}

class KeywordsForm(forms.Form):
	keywords_bulk = forms.CharField(max_length=250, help_text="comma separated keywords", 
			    widget=forms.Textarea, label="Keywords")
	def clean_keywords_bulk(self):
		data = self.cleaned_data["keywords_bulk"]
		# Убираем все цифры и специальные символы кроме & (для black & white)
		data = re.sub("[^a-zA-Z&,\s]", "", data)
		return data

class KeywordsEditForm(forms.Form):
	keywords_bulk = forms.CharField(max_length=250, help_text="comma separated keywords", 
			    widget=forms.Textarea, label="Keywords", required=False)
	def clean_keywords_bulk(self):
		data = self.cleaned_data["keywords_bulk"]
		# Убираем все цифры и специальные символы кроме & (для black & white)
		data = re.sub("[^a-zA-Z&,\s]", "", data)
		return data
	
class KeywordsCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
	template_name = "managephotos/widget_kwcheckbox.html"

class PhotoEditForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ["src", "src_min", "url", "url_min", "star", "genre", 
	    		"title", "place", "keywords"]
		CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),]
		labels = {
			'src': 'The path to the hires photo',
			'src_min': 'The path to the thumbnail',
			"star": 'The rank (priority) of the photo',
			'url': 'Friendly URL of the photo',
			'url_min': 'Friendly URL to the thumbnail'
		}
		widgets = {
			'star': forms.RadioSelect(choices=CHOICES),
			"keywords": KeywordsCheckboxSelectMultiple
		}					
