from django.db import models
from profiles.models import Profile
from django.utils import timezone
from django.core.exceptions import ValidationError


class Friend(models.Model):
    # Friends models
    to_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = ('Друг')
        verbose_name_plural = ('Друзья')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Користувач #{self.to_user_id} дружить з #{self.from_user_id}'

    def save(self, *args, **kwargs):
        # Users cannot be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError(
                'Користувачі не можуть дружити самі із собою.')
        super().save(*args, **kwargs)


    def add_friend(self, account):
        if not account in self.to_user.all():
            self.to_user.add(account)
            self.save()


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
    message = models.TextField("Message", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    viewed = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        verbose_name = 'Запрос на дружбу'
        verbose_name_plural = 'Запросы на дружбу'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Пользователь #{self.from_user_id} запросил дружбу с {self.to_user_id}'

    def accept(self):
        # update both sender and receiver friend list
        receiver_friend_list = Friend.objects.get(user=self.to_user)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.from_user)
            sender_friend_list = Friend.objects.get(user=self.from_user)
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