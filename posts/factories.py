# Third party
import factory
from factory.django import DjangoModelFactory

# Local apps
from posts.models import Author, Post


class PostFactory(DjangoModelFactory):
    """Create post objects with dummy data for testing.

    Extends:
        DjangoModelFactory
    """

    class Meta:
        model = Post

    # Relation
    author = Author.objects.get(pk=1)

    # NOTE: The passed argument -- first_name --  is related to the faker
    # library and not to Django or the Local apps, more examples here:
    # https://faker.readthedocs.io/en/master/providers/faker.providers.person.html

    # Normal columns
    title = factory.Faker('first_name')
    thumbnail = 'pexels-mike-170811.jpg'
    content = factory.Faker('sentence', nb_words=5, variable_nb_words=True)
