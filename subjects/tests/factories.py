from factory.django import DjangoModelFactory
from factory import SubFactory
from subjects.models import Semester, Subject, PreReq, Continence, Equivalence
from institutes.tests.factories import InstituteFactory


class SemesterFactory(DjangoModelFactory):
    class Meta:
        model = Semester
        django_get_or_create = ('semester', )

    semester = 1
    year = '2019'


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject
        django_get_or_create = ('initials', )

    initials = 'MC102'
    name = 'Algoritmos e Programação de Computadores'
    syllabus = 'Programação Básica'
    workload = 6
    institute = SubFactory(InstituteFactory)


class PreReqFactory(DjangoModelFactory):
    class Meta:
        model = PreReq
        django_get_or_create = ('initials', )

    initials = 'MC404 MC602'
    year_start = '2014'
    year_end = '2016'


class ContinenceFactory(DjangoModelFactory):
    class Meta:
        model = Continence
        django_get_or_create = ('initials', )

    initials = 'AL003'


class EquivalenceFactory(DjangoModelFactory):
    class Meta:
        model = Equivalence
        django_get_or_create = ('initials', )

    initials = 'EA869'
