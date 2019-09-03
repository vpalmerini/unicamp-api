from factory.django import DjangoModelFactory
from factory import SubFactory
from courses.models import Course, Specialization
from institutes.tests.factories import InstituteFactory


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ('id', )

    id = 42
    name = 'Ciência da Computação'
    shift = 'Noturno'
    institute = SubFactory(InstituteFactory)


class SpecializationFactory(DjangoModelFactory):
    class Meta:
        model = Specialization
        django_get_or_create = ('code', )

    code = 'AB'
    specialization = 'Azóide'
    course = SubFactory(CourseFactory)
