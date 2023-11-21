from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from profiles.models import Profile


class Post(models.Model):
    # Post model
    title = models.CharField(max_length=150)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, related_name="post_likes", blank=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def like(self, user):
        if user not in self.likes.all():
            self.likes.add(user)
        else:
            self.likes.remove(user)
    
    # def get_absolute_url(self):
    #     return reverse('post_create', kwargs={'pk':self.pk})
    

class Comments(models.Model):
    # Comments model
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='likes_comments', blank=True)
    reply = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)

    def total_clikes(self):
        return self.likes.count()
    
    def __str__(self):
        return f'{self.post.title} - {self.author.user.name} - {self.id}'