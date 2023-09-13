from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
]