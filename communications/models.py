from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='author_room', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_room', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}-{self.author}-{self.friend}'
    

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_messages', on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    has_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message + " " + str(self.date)