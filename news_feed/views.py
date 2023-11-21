from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from .models import Post
from .forms import PostCreateForm, CommentsCreateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class Mixin():
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionError
        return obj
    

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
        
    def get_success_url(self):
        user_id = self.request.user.id 
        return reverse('profile:public_profile', kwargs={'pk': user_id})
    
    
class AllPostView(ListView):
    # Output all news
    model = Post
    template_name = 'posts/news.html'
    context_object_name = 'posts'


class PostDeleteView(Mixin, DeleteView):
    # Delete post
    model = Post
    success_url = reverse_lazy('newsfeed:news')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class PostUpdateView(Mixin, UpdateView):
    # Update post
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('newsfeed:news')
    fields = ['title', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class LikePostView(View):
    # Likes on posts
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if request.user.is_authenticated:
            if request.user not in post.likes.all():
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)

            likes_count = post.total_likes()
            return JsonResponse({'likes': likes_count})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=400)


class CommentsCreateView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwakgs):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form = CommentsCreateForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.profile
            comment.save()

            return JsonResponse({'succes': 'Comment added successfully'})
        else:
            return JsonResponse({'error': 'Invalid form submission'}, status=400)