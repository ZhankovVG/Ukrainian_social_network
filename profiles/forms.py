from django import forms
from django.contrib.auth.models import User
from .models import Profile
from PIL import Image


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birthday', 'education', 'country', 'city', 'gender', 'avatar', 'phone']