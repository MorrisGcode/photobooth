from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from. models import Photo
from cloudinary.forms import CloudinaryFileField

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields =('username','email', 'password1', 'password2')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PhotoForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'resource_type': 'image',
            'folder': 'static/photos/',
            'allowed_formats': ['jpg', 'png', 'jpeg'],
        }
    )

    class Meta:
        model = Photo
        fields = ['image', 'title', 'description', 'tags']