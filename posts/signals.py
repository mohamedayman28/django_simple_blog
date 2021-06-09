# Django
from django.db import IntegrityError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

# Local Apps
from posts.models import Comment, Notification, Post


@receiver(post_save, sender=Comment)
def create_notification_on_new_comment(sender, instance, **kwargs):
    post = Post.objects.only('id').get(pk=instance.post_id)

    try:
        Notification.objects.create(
            post=post,
            comment_id=instance.id
        )
    # On UNIQUE constrains error, don't create object.
    except IntegrityError:
        pass


@receiver(post_delete, sender=Comment)
def delete_notification_on_post_delete(sender, instance, **kwargs):
    post = Post.objects.only('id').get(pk=instance.post_id)
    Notification.objects.filter(post=post).delete()
