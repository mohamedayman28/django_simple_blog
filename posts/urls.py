# Django
from django.urls import path

# Local Django
from posts import views


urlpatterns = [
    # Show all posts.
    path('', views.home_page, name='post_home_page'),
    # Create new post.
    path('create-post/', views.post_form, name='post_create'),
    # Get post details.
    path('post/<id>/', views.post_details, name='post_details'),
    # Create comment related to post.
    path('post/<id>/create-comment/', views.post_comment_create, name='post_comment_create'),
    # Update post.
    path('update-post/<id>/', views.post_form, name='post_update'),
    # Delete post
    path('delete-post/<id>/', views.post_form, name='post_delete'),

    # Filter posts by category.
    path('category/<category>/', views.home_page, name='post_category'),
]
