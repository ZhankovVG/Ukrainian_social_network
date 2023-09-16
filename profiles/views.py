from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, View
from .models import UserProfile
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm


class WelkomePage(ListView):
    # Start page
    model = UserProfile
    template_name = 'profiles/welcome_page.html'


class ProfileView(View):
    # User profile
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'profiles/profile.html', context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Ваша учетная запись обновлена!")
            return redirect('profile')

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'profiles/profile.html', context)


class PublicProfileView(View):
    # Creating a public profile view
    def get(self, request, username):
        user = UserProfile.objects.get(username=username)
        return render(request, 'profiles/public_profile.html', {"context": user})


class UserProfileView(ListView):
    # All user profiles
    model = UserProfile
    template_name = "profiles/all_profiles.html"
    context_object_name = "profiles"
    
    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)
    

class UserProfileDetailView(DetailView):
    # User profile details view
    model = UserProfile
    template_name = 'profiles/userprofile_dateil.html'

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)