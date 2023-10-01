from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('search/', views.FindFriendsView.as_view(), name='search'),
    path('send_friend_request/', views.SendFriendRequestView.as_view(), name='send_friend_request'),
]