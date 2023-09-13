from django.shortcuts import redirect
from django.views.generic import ListView
from .models import UserProfile


class UserProfileView(ListView):
    model = UserProfile