from django.urls import path
from .views import *

app_name = "communications"


urlpatterns = [
    path('message/', all_messages, name='all_messages'),
    path('chat/<int:friend_id>/', chat_with_friend, name='chat_with_friend'),
]