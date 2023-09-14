from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='detail'),
    path('', views.UserProfileView.as_view(), name='home'),
]