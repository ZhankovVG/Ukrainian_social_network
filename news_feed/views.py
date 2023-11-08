from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Post
from .forms import PostCreateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'
    success_url = '/' 

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def post(self, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_success_url(self):
        user_id = self.request.user.id 
        return reverse('profile:public_profile', kwargs={'pk': user_id})


class AllPostView(ListView):
    model = Post
    template_name = 'posts/news.html'
    context_object_name = 'posts'