from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('find_friends/', views.FindFriendsListView.as_view(), name="find_friends"),
    path('friend_requests/', views.FriendRequestsListView.as_view(), name="friend_requests"),
    path('send_friend_request/<int:user_id>/', views.SendFriendshipRequestView.as_view(), name='send_friend_request'),
    path('confirm_friend_request/<int:request_id>/', views.confirm_friend_request, name='confirm_friend_request'),
    path('cancel_friend_request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('all_friends/', views.FriendsListView.as_view(), name='all_friends'),
]