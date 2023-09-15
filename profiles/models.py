from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    # User model
    GENDER = (
        ('male', 'мужчина'),
        ('female', 'женщина'),
        ('animal', 'зверюшка'),
    )
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=7, choices=GENDER, default='animal', blank=True)
    city = models.CharField(max_length=20, blank=True)
    is_online = models.BooleanField(default=False)
    country = models.CharField(max_length=20, blank=True)
    education = models.CharField(max_length=50, default='', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



class Status(models.Model):
    # Status
    text = models.CharField(max_length=400)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'