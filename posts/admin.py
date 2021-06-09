# Django
from django.contrib import admin

# Local apps
from posts.models import Author, Category, Comment, Post


admin.site.register(Author)
admin.site.register(Category)


class CommentInline(admin.StackedInline):
    """
    Inlines with PostAdmin.
    """
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['title', 'created_time']
    list_filter = ['author']
