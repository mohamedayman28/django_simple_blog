# Django
from django.urls import path

# Local apps
from posts import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post-author/', views.post_related_to_author, name='post_related_to_author'),
    path('post-create/', views.post_create, name='post_create'),
    path('post-search/', views.post_search, name='post_search'),
    path('post-delete/<int:id>/', views.post_delete, name='post_delete'),
    path('post-update/<int:id>/', views.post_update, name='post_update'),
    path('post/<int:id>/comment-create/', views.comment_create, name='comment_create'),
    path('post/<int:id>/', views.post_details, name='post_details'),
    path('post/<str:category>/', views.post_filter_by_category, name='post_filter_by_category'),

    path('notification/', views.notification_list, name='notification_list'),
    path('notification/<int:id>/', views.notification_details, name='notification_details'),
]
