from factory.django import DjangoModelFactory
from factory import SubFactory
from professors.models import Professor
from institutes.tests.factories import InstituteFactory


class ProfessorFactory(DjangoModelFactory):
    class Meta:
        model = Professor
        django_get_or_create = ('name', )

    name = 'Pedro Rezende'
    web_page = 'https://www.ic.unicamp.br/~rezende/'
    institute = SubFactory(InstituteFactory)
