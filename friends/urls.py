from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('find_friends/', views.FindFriendsView.as_view(), name="find_friends"),
    path('friend_requests/', views.FriendRequestsListView.as_view(), name="friend_requests"),
    path('send_friend_request/<int:user_id>/', views.SendFriendshipRequestView.as_view(), name='send_friend_request'),
    path('confirm_friend_request/<int:request_id>/', views.ConfirmFriendRequestView.as_view(), name='confirm_friend_request'),
    path('cancel_friend_request/<int:request_id>/', views.DeleteFriendRequestView.as_view(), name='cancel_friend_request'),
    path('all_friends/', views.FriendsListView.as_view(), name='all_friends'),
    path('remove_friend/<int:friend_id>/', views.RemoveFriendView.as_view(), name='remove_friend'),
]