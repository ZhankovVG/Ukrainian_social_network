from django.shortcuts import render
from django.views.generic import ListView
from .models import Friend


class FindFriendsListView(ListView):
    model = Friend
    context_object_name = 'users'
    template_name = ''

   