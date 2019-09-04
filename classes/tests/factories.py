from factory.django import DjangoModelFactory
from factory import SubFactory
from classes.models import Class, Schedule
from subjects.tests.factories import SubjectFactory


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = Class
        django_get_or_create = ('class_id', )

    class_id = 'A'
    positions = 30
    enrolled = 28
    subject = SubFactory(SubjectFactory)


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = Schedule
        django_get_or_create = ('day', )

    day = 'Segunda'
    time_start = '10:00'
    time_end = '12:00'
    place = 'CB01'
    class_id = SubFactory(ClassFactory)
