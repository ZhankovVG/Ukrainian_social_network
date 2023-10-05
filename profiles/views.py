from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class WelcomePageView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {'username': request.user.username}
        return render(request, 'profiles/welcome_page.html', context)


class PublicProfileView(DetailView):
    model = Profile
    template_name = 'profiles/public_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.object.username 
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
            return redirect('/welcome_page/')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user)
    return render(request, 'profiles/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})