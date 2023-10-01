from django.shortcuts import render, redirect
from .models import Friend, FriendshipRequest
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from django.views.generic import View, ListView
from django.db.models import Q
from django.http import JsonResponse
from .forms import FriendshipRequestForm


class FindFriendsView(ListView):
    # Friend search
    template_name = 'friends/find_friends.html'

    def get(self, request):
        search_query = self.request.GET.get('search')

        if search_query:
            users = Profile.objects.filter(
            Q(username__icontains=search_query) | Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            ).exclude(username=request.user.username)
        else:
            users = Profile.objects.exclude(username=request.user.username)

        return render(request, self.template_name, {'users': users})
     
        
class SendFriendRequestView(View):
    # Friend request
    def post(self, request):
        form = FriendshipRequestForm(request.POST)
        if form.is_valid():
            user_to_add_id = form.cleaned_data['user_to_add_id']
            user_to_add = Profile.objects.get(pk=user_to_add_id)
            FriendshipRequest.objects.create(
                from_user=request.user,
                to_user=user_to_add,
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})