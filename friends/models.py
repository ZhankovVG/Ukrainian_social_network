from django.db import models
from profiles.models import Profile
from django.utils import timezone
from django.core.exceptions import ValidationError


class FriendshipManager(models.Manager):
    # Friendship manager

    def friends(self, user):
        # Return a list of all friends
        qs = (
            Friend.objects.select_related('from_user', 'to_user')
                .filter(to_user=user)
                .all()
        )
        friends = [u.from_user for u in qs]
        return friends
    
    def requests(self, user):
        # Return a list of friendship requests
        qs = (
            FriendshipRequest.objects.select_related('from_user', 'to_user')
                .filter(to_user=user)
                .all()
        )
        requests = list(qs)
        return requests
    
    def send_requests(self, user):
        # Return a list of friendship requests from user
        qs = (
            FriendshipRequest.objects.select_related('from_user', 'to_user')
                .filter(to_user=user)
                .all()
        )
        requests = list(qs)
        return requests
    
    def got_friend_requests(self, user):
        # Return a list of friendship requests user got
        qs = (
            FriendshipRequest.objects.select_related('from_user__profile', 'to_user')
                .filter(to_user=user)
                .all()
        )
        unread_requests = list(qs)
        return unread_requests


class Friend(models.Model):
    to_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзі'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Користувач #{self.to_user_id} дружить з #{self.from_user_id}'

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError(
                'Користувачі не можуть дружити самі із собою.')
        super().save(*args, **kwargs)


class FriendshipRequest(models.Model):
    # Model to represent friendship requests
    from_user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friendship_requests_sent'
    )
    to_user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friendship_requests_received'
    )
    message = models.TextField("Повідомлення", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    viewed = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Запит на дружбу'
        verbose_name_plural = 'Запити на дружбу'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Користувач #{self.from_user_id} надіслав запит на дружбу #{self.to_user_id}'

    def accept(self):
        receiver_friend_list = Friend.objects.get(from_user=self.to_user)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.from_user)
            sender_friend_list = Friend.objects.get(from_user=self.from_user)
            if sender_friend_list:
                sender_friend_list.add_friend(self.to_user)
            self.is_active = False
            self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()