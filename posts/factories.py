"""
NOTE: The passed argument -- first_name --  is related to the faker
library and not to Django or the Local apps, more examples here:
https://faker.readthedocs.io/en/master/providers/faker.providers.person.html
"""


# Third party
import factory
from factory.django import DjangoModelFactory

# Django
from django.contrib.auth.models import User

# Local apps
from posts.models import Author, Comment, Notification, Post


class PostFactory(DjangoModelFactory):
    """
    Create post objects with dummy data for testing.

    Usage, open Django shell and
        for i in range(10):
            PostFactory()
    """
    class Meta:
        model = Post

    # Assuming that Author is exist, or you have to create one.
    author = Author.objects.get(pk=1)

    title = factory.Faker('first_name')
    thumbnail = 'pexels-mike-170811.jpg'
    content = factory.Faker('sentence', nb_words=5, variable_nb_words=True)


class CommentFactory(DjangoModelFactory):
    """
    Create post objects with dummy data for testing.

    Usage, open Django shell and
        for i in range(10):
            CommentFactory()
    """
    class Meta:
        model = Comment

    # Assuming that Post and User are exist, or you have to create one.
    post = Post.objects.get(id=2)
    commenter = User.objects.get(pk=1)

    content = factory.Faker('sentence', nb_words=5, variable_nb_words=True)


class NotificationFactory(DjangoModelFactory):
    """
    Create notification objects with dummy data for testing.

    Usage, open Django shell and
        for i in range(10):
            NotificationFactory()
    """
    class Meta:
        model = Notification

    # Assuming that User is exist, or you have to create one.
    receiver = User.objects.get(pk=1)

    feedback_to_user = factory.Faker('sentence', nb_words=5, variable_nb_words=True)
    sender_model_id = factory.Faker('sentence', nb_words=5, variable_nb_words=True)
