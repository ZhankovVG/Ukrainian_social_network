from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    image = forms.ImageField(label=('Image'), error_messages = {'invalid':("Image files only")}, widget=forms.FileInput, required=False)
    class Meta:
        model = UserProfile
        fields = ['bio', 'birthday', 'education', 'country', 'city', 'gender', 'birthday', 'avatar', 'phone']
        widgets = {
            'user': forms.HiddenInput(),  # Скрываем поле user в форме
        }