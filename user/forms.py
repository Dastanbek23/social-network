from tkinter import Image

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Photo


class UserRegisterForm(UserCreationForm):
    username = forms.TextInput()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'description')
        widgets = {
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        if not image:
            raise forms.ValidationError('Please upload an image')
        return image

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if not bio:
            raise forms.ValidationError('Please upload a bio')
        return bio