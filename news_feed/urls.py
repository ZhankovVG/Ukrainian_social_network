from django.urls import path
from . import views

app_name = "newsfeed"

urlpatterns = [
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('news/', views.AllPostView.as_view(), name='news'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
]