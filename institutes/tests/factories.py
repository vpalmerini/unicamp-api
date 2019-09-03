from factory.django import DjangoModelFactory
from institutes.models import Institute


class InstituteFactory(DjangoModelFactory):
    class Meta:
        model = Institute
        django_get_or_create = ('initials', )

    initials = 'IC'
    name = 'Instituto de Computação'
