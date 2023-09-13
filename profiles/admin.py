from django.contrib import admin
from .models import UserProfile, Status


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'middle_name', 
        'phone', 
        'avatar', 
        'birthday', 
        'gender',
)
    list_filter = ('birthday', 'gender',)
    readonly_fields = ('phone', )


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('text', )