from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import UserProfile


class WelcomePageView(View):
    # Start page
    def get(self, request):
        return render(request, 'profiles/welcome_page.html')


class UserProfilelView(ListView):
    # User profile details view
    model = UserProfile
    template_name = 'profiles/userprofile_list.html'

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)


class PublicProfileView(View):
    # Creating a public profile view
    def get(self, request, username):
        user = get_object_or_404(UserProfile, username=username)
        return render(request, 'profiles/public_profile.html', {"context": user})