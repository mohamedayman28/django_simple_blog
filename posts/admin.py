# Django
from django.contrib import admin

# Local apps
from posts.models import Author, Category, Comment, Post

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
