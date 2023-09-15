from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, View
from .models import UserProfile


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