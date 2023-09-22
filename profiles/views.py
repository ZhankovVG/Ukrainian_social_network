from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Profile
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
        user = get_object_or_404(User, username=username)
        return render(request, 'profiles/public_profile.html', {"context": user})


def edit_profile(request):
    try:
        user_profile = request.user.userprofile
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            if user_profile:
                p_form.save()
            else:
                profile_data = {'user': request.user}
                p_form = ProfileUpdateForm(request.POST, request.FILES, initial=profile_data)
                if p_form.is_valid():
                    p_form.save()
            messages.success(request, "Профіль успішно оновлено!")
        else:
            messages.error(request, "Профіль не оновлено. Введіть правильні дані!")
        return redirect('profiles:edit_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if user_profile:
            p_form = ProfileUpdateForm(instance=user_profile)
        else:
            profile_data = {'user': request.user}
            p_form = ProfileUpdateForm(initial=profile_data)

    args = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'profiles/edit_profile.html', args)

