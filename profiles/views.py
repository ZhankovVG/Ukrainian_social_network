from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View, UpdateView
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy


class WelcomePageView(View):
    # Start page
    def get(self, request):
        return render(request, 'profiles/welcome_page.html')


class ProfileListAllView(ListView):
    # All user profiles
    model = Profile
    template_name = 'profiles/userprofile_list.html'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)


class ProfileDetailView(DetailView):
    # User profile details view
    model = Profile
    template_name = 'profiles/profile_details.html'
    context_object_name = 'user'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Profile, pk=pk)


class PublicProfileView(View):
    # Creating a public profile view
    def get(self, request, username):
        user = get_object_or_404(Profile, username=username)
        return render(request, 'profiles/public_profile.html', {"context": user})


@login_required
def ProfileEditView(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect(reverse_lazy('profiles:edit-profile'))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'profiles/edit-my-profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })