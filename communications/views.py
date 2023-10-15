import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.utils.safestring import mark_safe

from profiles.models import Profile
from friends.models import Friend


@login_required(login_url=_("accounts:login"))
def all_messages(request):
    friends = Friend.objects.friends(request.user)
    return render(request, "communications/all-messages.html", {'friends': friends})


# Conversation with one friend
@login_required(login_url=_("accounts:login"))
def messages_with_one_friend(request, friend):
    if request.user.username == friend:
        return redirect(_('communications:all-messages'))
    try:
        if not Profile.objects.get(username=friend):
            return redirect(_('communications:all-messages'))
    except:
        return redirect(_('communications:all-messages'))
    friend_user = Profile.objects.get(username=friend)
    if not Friend.objects.are_friends(request.user, friend_user):
        return redirect(_('communications:all-messages'))
    friends = Friend.objects.friends(request.user)
    return render(request, "communications/friend-messages.html", {
        'friends': friends,
        'friend_user': friend_user,
        'friend_name_json': mark_safe(json.dumps(friend)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
