from django import forms
from .models import Post, Comments


class PostCreateForm(forms.ModelForm):
    # Post form
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']


class CommentsCreateForm(forms.ModelForm):
    # Comment form
    class Meta:
        model = Comments
        fields = ['name', 'content']