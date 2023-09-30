from django.shortcuts import render, redirect
from .models import Friend
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from django.views.generic import View, ListView
from django.db.models import Q



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
    

@login_required
class SendFriendRequestView(View):
    # Adding friends
    def post(self, request, user_id):
        user_to_add = Profile.objects.get(id=user_id)

        friend_request, created = Friend.objects.get_or_create(
            from_user=request.user,
            to_user=user_to_add.user,
        )

        if created:
            return redirect('find_friends')
        else:
            return redirect('find_friends')
        
        
@login_required
class FriendRequestListView(ListView):
    # Get all friend requests current user got
    model = Friend
    context_object_name = 'friend_requests'
    template_name = 'friends/friend_requests.html'