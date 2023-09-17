from django.urls import path
from . import views


urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='welcome_page'),
    path('profiles/<int:pk>/', views.UserProfilelView.as_view(), name='profile_detail_view'),
    path('public_profile/<int:pk>/', views.PublicProfileView.as_view(), name='public_profile'),   
]