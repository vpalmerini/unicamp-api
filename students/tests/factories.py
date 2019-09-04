from factory.django import DjangoModelFactory
from factory import SubFactory
from students.models import Student
from courses.tests.factories import CourseFactory


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student
        django_get_or_create = ('ra', )

    ra = '100000'
    name = 'Victor Palmerini'
    email = 'v100000@dac.unicamp.br'
    course = SubFactory(CourseFactory)
