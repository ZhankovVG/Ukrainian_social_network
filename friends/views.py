from django.shortcuts import render, redirect
from .models import Friend, FriendshipRequest
from profiles.models import Profile
from django.views.generic import View, ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages


class FindFriendsListView(LoginRequiredMixin, ListView):
    # Search friends
    model = Friend
    context_object_name = 'users'
    template_name = "friends/find_friends.html"

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        current_user_friends = self.request.user.friends.values('id')
        sent_request = list(
            FriendshipRequest.objects.filter(Q(from_user=self.request.user))
            .exclude(to_user=self.request.user.id)
            .values_list('to_user_id', flat=True))

        users = Profile.objects.exclude(id__in=current_user_friends).exclude(id__in=sent_request).exclude(
            id=self.request.user.id)
        if search_query:
            users = users.filter(username__icontains=search_query)

        return users
     
        
class FriendRequestsListView(LoginRequiredMixin, ListView):
    # Get all friend requests current user got
    model = Friend
    context_object_name = 'friend_requests'
    template_name = 'friends/friend_requests.html'

    def get_queryset(self):
        return Friend.objects.got_friend_requests(user=self.request.user)
    

class SendFriendshipRequestView(View):
    def post(self, request, user_id):
        target_user = get_object_or_404(Profile, id=user_id)

        existing_request = FriendshipRequest.objects.filter(
            from_user=request.user,
            to_user=target_user,
            is_active=True
        ).first()

        if existing_request:
            messages.error(
                request,
                "Ви вже надіслали запит на дружбу цьому користувачу."
            )
        else:
            FriendshipRequest.objects.create(
                from_user=request.user,
                to_user=target_user,
                is_active=True
            )
            messages.success(
                request,
                "Запит на дружбу надіслано успішно."
            )

        return redirect('welcome_page', user_id=user_id)
