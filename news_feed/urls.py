from django.urls import path
from . import views

app_name = "newsfeed"

urlpatterns = [
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('news/', views.AllPostView.as_view(), name='news'),
]