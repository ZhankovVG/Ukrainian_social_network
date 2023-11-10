from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DeleteView
from .models import Post
from .forms import PostCreateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class PostCreateView(CreateView):
    # Create new post
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
    # Output all news
    model = Post
    template_name = 'posts/news.html'
    context_object_name = 'posts'


class PostDeleteView(DeleteView):
    # Delete post
    model = Post
    success_url = reverse_lazy('newsfeed:news')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionError
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())
