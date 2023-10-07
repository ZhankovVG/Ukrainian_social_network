from django.db import models
from profiles.models import Profile
from django.utils import timezone
from django.core.exceptions import ValidationError
from friends.exceptions import AlreadyFriendsError, AlreadyExistsError
from django.db.models import Q


class FriendshipManager(models.Manager):
    # Friendship manager

    def friends(self, user):
        # Return a list of all friends
        qs = (
            Friend.objects.filter(to_user=user)
                .all()
        )
        friends = [u.from_user for u in qs]

        return friends

    def requests(self, user):
        # Return a list of friendship requests
        qs = (
            FriendshipRequest.objects.filter(to_user=user)
                .all()
        )
        requests = list(qs)

        return requests

    def sent_requests(self, user):
        # Return a list of friendship requests from user
        qs = (
            FriendshipRequest.objects.filter(from_user=user)
                .all()
        )
        requests = list(qs)

        return requests

    def got_friend_requests(self, user):
        # Return a list of friendship requests user got
        qs = (
            FriendshipRequest.objects.filter(to_user=user)
                .all()
        )
        unread_requests = list(qs)
        return unread_requests

    def unread_requests(self, user):
        # Return a list of unread friendship requests
        qs = (
            FriendshipRequest.objects.filter(to_user=user, viewed__isnull=True)
                .all()
        )
        unread_requests = list(qs)

        return unread_requests

    def unread_request_count(self, user):
        # Return a count of unread friendship requests
        count = FriendshipRequest.objects.filter(to_user=user, viewed__isnull=True).count()
        return count

    def read_requests(self, user):
        # Return a list of read friendship requests
        qs = (
            FriendshipRequest.objects.filter(to_user=user, viewed__isnull=False)
                .all()
        )
        read_requests = list(qs)

        return read_requests

    def rejected_requests(self, user):
        # Return a list of rejected friendship requests
        qs = (
            FriendshipRequest.objects.filter(to_user=user, rejected__isnull=False)
                .all()
        )
        rejected_requests = list(qs)

        return rejected_requests

    def unrejected_requests(self, user):
        # All requests that haven't been rejected
        qs = (
            FriendshipRequest.objects.filter(to_user=user, rejected__isnull=True)
                .all()
        )
        unrejected_requests = list(qs)

        return unrejected_requests

    def unrejected_request_count(self, user):
        # Return a count of unrejected friendship requests
        count = FriendshipRequest.objects.filter(to_user=user, rejected__isnull=True).count()
        return count

    def add_friend(self, from_user, to_user, message=None):
        # Create a friendship request
        if from_user == to_user:
            raise ValidationError("Користувачі не можуть дружити самі із собою.")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Користувачі вже є друзями.")

        if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise AlreadyExistsError("Ви вже просили дружбу у цього користувача.")

        if FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
            raise AlreadyExistsError("Цей користувач вже просив у вас дружбу.")

        if message is None:
            message = ""

        request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )

        if created is False:
            raise AlreadyExistsError("Дружба вже запрошена.")

        if message:
            request.message = message
            request.save()

        return request

    def remove_friend(self, from_user, to_user):
        # Destroy a friendship relationship
        try:
            qs = Friend.objects.filter(
                Q(to_user=to_user, from_user=from_user) | Q(to_user=from_user, from_user=to_user))
            distinct_qs = qs.distinct().all()

            if distinct_qs:
                qs.delete()
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def are_friends(self, user1, user2):
        # Are these two users friends?
        try:
            Friend.objects.get(to_user=user1, from_user=user2)
            return True
        except Friend.DoesNotExist:
            return False


class Friend(models.Model):
    to_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = FriendshipManager()

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
        # Accept this friendship request
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

        self.delete()

        # Delete any reverse requests
        FriendshipRequest.objects.filter(
            from_user=self.to_user, to_user=self.from_user
        ).delete()

        return True

    def cancel(self):
        # Cancel this friendship request
        self.delete()
        return True