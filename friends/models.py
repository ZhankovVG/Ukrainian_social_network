from django.db import models
from profiles.models import Profile
from django.utils import timezone
from django.core.exceptions import ValidationError


class Friend(models.Model):
    # Friends models
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = ('Друг')
        verbose_name_plural = ('Друзья')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Користувач #{self.to_user_id} дружить з #{self.from_user_id}'
    
    def save(self, *args, **kwargs):
        # Users cannot be friends with themselves
        if self.to_user ==self.from_user:
            raise ValidationError('Користувачі не можуть дружити самі із собою.')
        super().save(*args, **kwargs)