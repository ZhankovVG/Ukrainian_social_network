from django.urls import path
from . import views


urlpatterns = [
    path('', views.WelkomePage.as_view(), name='home'),
    path('all/', views.UserProfileView.as_view(), name='profile-list-view'),
    path('<int:pk>/', views.UserProfileDetailView.as_view(), name='profile-detail-view'),
    path('public-profile/<str:username>/', views.PublicProfileView.as_view(), name='public-profile'),
]