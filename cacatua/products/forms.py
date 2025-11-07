from django import forms
from . import models

class UploadProduct(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name','price','description','category']
