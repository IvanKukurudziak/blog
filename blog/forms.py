from django import forms
from .models import Post, Comment
from .models import Post

from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('topic', 'title', 'post_img', 'text', 'link')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ComentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_text',)





