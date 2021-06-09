# Django
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db import models


# Third party
from filebrowser.fields import FileBrowseField
from tinymce import HTMLField


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Authors'


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category)

    title = models.CharField(max_length=50)
    thumbnail = FileBrowseField(max_length=200, null=True)
    content = HTMLField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['content']),
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title

    def get_create_url(self):
        return reverse('post_create', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post_update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'id': self.id})

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'id': self.id})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    username = models.CharField(max_length=20)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = 'Comments'


class Notification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment_id = models.CharField(max_length=20, unique=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Notifications'

    def get_feedback_message(self):
        """
        Telling what notification is about.
        """
        return f"{self.post.title.title()} post, has new comment."

    def get_absolute_url(self):
        """
        Jump directly to comment.

        - if Post.id = 1
        - and related Comment.id = 24
        - get_absolute_url returns /post/1/#2.
        """
        return reverse('post_details', kwargs={'id': self.post_id}) + "#" +\
            self.comment_id
