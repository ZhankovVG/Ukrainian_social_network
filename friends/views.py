from django.shortcuts import render, redirect
from .models import Friend, FriendshipRequest
from profiles.models import Profile
from django.views.generic import View, ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages


class FriendsListView(LoginRequiredMixin, ListView):
    # All friends
    model = Friend
    context_object_name = 'friends'
    template_name = 'friends/all_friends.html'

    def get_queryset(self):
        return Friend.objects.friends(self.request.user)
    

class FindFriendsView(LoginRequiredMixin, ListView):
    # Search friends
    model = Profile
    context_object_name = 'users'
    template_name = "friends/find_friends.html"

    def get_queryset(self):
        query = self.request.GET.get('search')
        current_user = self.request.user
        current_user_friends = Friend.objects.friends(current_user)

        if query:
            found_friends = Profile.objects.exclude(id=current_user.id).exclude(id__in=[friend.id for friend in current_user_friends])
            found_friends = found_friends.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).distinct()
        else:
            found_friends = Profile.objects.none()

        return found_friends
     
        
class FriendRequestsListView(LoginRequiredMixin, ListView):
    # Get all friend requests current user got
    model = Friend
    context_object_name = 'friend_requests'
    template_name = 'friends/friend_requests.html'

    def get_queryset(self):
        return Friend.objects.got_friend_requests(user=self.request.user)


class SendFriendshipRequestView(View):
    # Friend request
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

        return redirect('friends:find_friends')


class ConfirmFriendRequestView(View):
    # Accept request
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendshipRequest, pk=request_id)

        if friend_request.to_user != request.user:
            messages.error(request, "Вы не можете подтвердить этот запрос на дружбу.")
            return redirect('friends:confirm_friend_request')

        friend_request.accept()
        messages.success(request, f"Запрос на дружбу с {friend_request.from_user} подтвержден.")

        referring_url = request.META.get('HTTP_REFERER', 'friends:confirm_friend_request')
        return redirect(referring_url)


class DeleteFriendRequestView(View):
    # Delete friends
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendshipRequest, pk=request_id)

        if friend_request.to_user != request.user:
            messages.error(request, "Вы не можете отклонить этот запрос на дружбу.")
        else:
            friend_request.cancel()
            messages.success(request, "Запрос на дружбу удален.")

        referring_url = request.META.get('HTTP_REFERER', 'friends:cancel_friend_request')
        return redirect(referring_url)
    

class DeclineFriendshipRequestView(View):
    # Cancel request friends
    def get(self, request, request_id):
        friendship_request = get_object_or_404(FriendshipRequest, pk=request_id)

        if friendship_request.to_user == request.user and friendship_request.is_active:
            friendship_request.decline()
            messages.error(request, "Вы не можете отклонить этот запрос на дружбу.")
        else:
            friendship_request.cancel()
            messages.success(request, "Запрос на дружбу удален.")

        referring_url = request.META.get('HTTP_REFERER', 'friends:cancel_friend_request')
        return redirect(referring_url)