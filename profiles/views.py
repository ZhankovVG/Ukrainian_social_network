from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import UserProfile
from django.contrib.auth.models import User


class WelcomePageView(View):
    # Start page
    def get(self, request):
        return render(request, 'profiles/welcome_page.html')


class ProfileListAllView(ListView):
    # All user profiles
    model = UserProfile
    template_name = 'profiles/userprofile_list.html'

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)


class ProfileDetailView(DetailView):
    # Creating a public profile view
    model = UserProfile
    template_name = 'profiles/profile_details.html'
    context_object_name = 'user'

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        return get_object_or_404(UserProfile, pk=pk)
    

class PublicProfileView(View):
    # Creating a public profile view
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, 'profiles/public_profile.html', {"context" : user})