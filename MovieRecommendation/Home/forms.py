from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

from Home.models import Product, Additional_image


class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','date_joined','last_login']
        labels ={'email':'Email'}

from django import forms
from .models import Product, Category




 # Import CKEditorWidget for RichTextField

from django import forms
from .models import Product
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # Import CKEditorUploadingWidget for RichTextField with image upload

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'categories', 'youtube', 'download', 'tags']
        widgets = {
            'categories': forms.CheckboxSelectMultiple
        }



