# Django
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

# Third party
from filebrowser.fields import FileBrowseField
from tinymce import HTMLField


class Author(models.Model):
    # Relation
    name = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Author'

    def __str__(self):
        return self.name.username


class Category(models.Model):
    # Relation
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name


class Post(models.Model):
    # Relation
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category)
    # Attributes
    title = models.CharField(max_length=50)
    thumbnail = FileBrowseField(max_length=200, null=True)
    content = HTMLField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Post'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'id': self.id})

    def get_create_url(self):
        return reverse('post_create', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post_update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'id': self.id})


class Comment(models.Model):
    # Relation
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Attributes
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.commenter.username

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Comment'
