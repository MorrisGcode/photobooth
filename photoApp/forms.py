from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from. models import Photo, UserProfile
from cloudinary.forms import CloudinaryFileField

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields =('username','email', 'password1', 'password2')

class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Tell us about yourself...'
        }),
        required=False
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Save the profile
            profile.save()
            # Update the user model
            user = profile.user
          
            user.save()
        return profile

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