from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    # Updates to user data
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    # Profile data updates
    class Meta:
        model = Profile
        fields = ['bio', 'birthday', 'education', 'country', 'city', 'gender', 'avatar', 'phone']