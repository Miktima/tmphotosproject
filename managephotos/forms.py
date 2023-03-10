from django import forms
from .models import Photo
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ["src", "src_min", "star", "genre", "title", "place"]

class KeywordsForm(forms.Form):
	keywords = forms.CharField(help_text="comma separated keywords")

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
