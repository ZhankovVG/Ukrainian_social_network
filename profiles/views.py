from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# class UserProfileView(ListView):
#     model = UserProfile

@method_decorator(login_required, name='dispatch')
class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'profiles/profile_detail.html'


class UserProfileView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        return context