from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class WelcomePageView(View):
    # Start page
    def get(self, request):
        return render(request, 'profiles/welcome_page.html')


class PublicProfileView(View):
    # Creating a public profile view
    @method_decorator(login_required)
    def get(self, request, username):
        user = get_object_or_404(Profile, username=username)
        return render(request, 'profiles/public_profile.html', {"context": user})


@login_required
def ProfileEditView(request):
    # Apdate data users
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('welcome_page')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user)
    return render(request, 'profiles/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})