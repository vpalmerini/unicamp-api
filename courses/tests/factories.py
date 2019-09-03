from factory.django import DjangoModelFactory
from factory import SubFactory
from courses.models import Course
from institutes.tests.factories import InstituteFactory


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ('id', )

    id = 42
    name = 'Ciência da Computação'
    shift = 'Noturno'
    institute = SubFactory(InstituteFactory)
