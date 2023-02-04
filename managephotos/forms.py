from django.forms import ModelForm
from .models import Src

class UploadImageForm(ModelForm):
	class Meta:
		model = Src
		fields = ["src"]