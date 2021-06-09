# Django
from django.forms import ModelForm

# Local apps
from posts.models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'content', 'categories')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
