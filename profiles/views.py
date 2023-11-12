from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from friends.views import FriendsListView
from django.dispatch import receiver 
from django.contrib.auth.signals import user_logged_in, user_logged_out
from news_feed.models import Post


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    if hasattr(user, 'profile'):
        user.profile.is_online = True
        user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    if hasattr(user, 'profile'):
        user.profile.is_online = False
        user.profile.save()


class WelcomePageView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'profiles/welcome_page.html')


class Mixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = self.object.id == self.request.user.id
        context['friends'] = self.get_friends_list()
        context['is_online'] = self.object.is_online
        
        return context


class PublicProfileView(Mixin, DetailView):
    model = Profile
    template_name = 'profiles/public_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'
    object = None

    def get_friends_list(self):
        friends_list = FriendsListView(request=self.request).get_queryset()
        return friends_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = Post.objects.filter(author=self.object).order_by('-date_posted')  # Retrieve the user's posts
        context['user_posts'] = user_posts
        return context
    
    
def ProfileEditView(request):
    # Apdate data users
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            updated_user_id = user.id
            return redirect(reverse('profile:public_profile', kwargs={'pk': updated_user_id}))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user)
    return render(request, 'profiles/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})