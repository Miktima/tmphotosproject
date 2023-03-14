from django import forms
from .models import Photo
import re


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ["src", "src_min", "star", "genre", "title", "place"]

class KeywordsForm(forms.Form):
	keywords = forms.CharField(max_length=250, help_text="comma separated keywords", 
			    widget=forms.Textarea)
	def clean_reywords(self):
		data = self.cleaned_data["keywords"]
		# Убираем все цифры и специальные символы кроме & (для black & white)
		data = re.sub("[^a-zA-Z&,\s]", "", data)
		return data

class PhotoEditForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ["src", "src_min", "url", "url_min", "star", "genre", 
	    		"title", "place", "keywords"]
