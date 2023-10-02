from django.shortcuts import render, redirect
from .models import Friend, FriendshipRequest
from profiles.models import Profile
from django.views.generic import View, ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class FindFriendsListView(LoginRequiredMixin, ListView):
    model = Friend
    context_object_name = 'users'
    template_name = "friends/find_friends.html"

    def get_queryset(self):
        current_user_friends = self.request.user.friends.values('id')
        sent_request = list(
            FriendshipRequest.objects.filter(Q(from_user=self.request.user))
            .exclude(to_user_id=self.request.user.id)
            .values_list('to_user_id', flat=True))
        users = Profile.objects.exclude(id__in=current_user_friends).exclude(id__in=sent_request).exclude(
            id=self.request.user.id)
        return users
     
        
class FriendRequestsListView(LoginRequiredMixin, ListView):
    # Get all friend requests current user got
    model = Friend
    context_object_name = 'friend_requests'
    template_name = 'friends/friend_requests.html'

    def get_queryset(self):
        return Friend.objects.got_friend_requests(user=self.request.user)