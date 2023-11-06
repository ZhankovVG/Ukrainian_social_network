from django.shortcuts import render
from django.views.generic import CreateView
from .models import Post
from .forms import PostCreateForm


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html' 
    success_url = '/success/'