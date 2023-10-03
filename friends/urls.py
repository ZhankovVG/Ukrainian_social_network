from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('find_friends/', views.FindFriendsListView.as_view(), name="find_friends"),
    path('friend_requests/', views.FriendRequestsListView.as_view(), name="friend_requests"),
    path('send_friend_request/<int:user_id>/', views.SendFriendshipRequestView.as_view(), name='send_friend_request'),
]