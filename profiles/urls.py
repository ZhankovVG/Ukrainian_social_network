from django.urls import path
from . import views



urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='welcome_page'),  
    path('public_profile/<str:username>/', views.PublicProfileView.as_view(), name='public_profile'),
    path('edit_profile/', views.ProfileEditView, name="edit_profile"),
]