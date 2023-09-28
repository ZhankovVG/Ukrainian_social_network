from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('find_friends/', views.SendFriendRequestView, name='find_friends'),
    path('search/', views.FindFriendsView.as_view(), name='search'),
]