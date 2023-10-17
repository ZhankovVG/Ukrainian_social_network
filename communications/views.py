from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy as _
from friends.models import Friend
from .models import Message, Room
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404
from django.db.models import Q


@login_required(login_url=_("accounts:login"))
def all_messages(request):
    # Output all messages
    friends = Friend.objects.friends(request.user)
    return render(request, "communications/all-messages.html", {'friends': friends})


@login_required(login_url=_("accounts:login"))
def chat_with_friend(request, friend_id):
    # Texting a friend
    friend = get_object_or_404(User, id=friend_id)
    room, created = Room.objects.get_or_create(author=request.user, friend=friend)

    if request.method == 'POST':
        message_text = request.POST.get('message', '')
        if message_text:
            message = Message(room=room, author=request.user, friend=friend, message=message_text)
            message.save()

    messages = Message.objects.filter(Q(room=room), (Q(author=request.user) | Q(friend=friend)))


    return render(request, 'communications/friend_messages.html', {'room': room, 'messages': messages})