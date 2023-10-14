from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from friends.models import Friend
from friends.views import FriendsListView


class WelcomePageView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {'username': request.user.username}
        return render(request, 'profiles/welcome_page.html', context)


class Mixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.object.username
        context['friends'] = self.get_friends_list()
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