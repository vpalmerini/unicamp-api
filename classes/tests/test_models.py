from django.test import TestCase
from classes.models import Class, Schedule
from subjects.tests.factories import SemesterFactory, SubjectFactory
from classes.tests.factories import ClassFactory, ScheduleFactory


class BaseModelTest(TestCase):
    def setUp(self):
        semester = SemesterFactory()
        subject = SubjectFactory()
        semester.subjects.add(subject)
        schedule = ScheduleFactory()


class ClassModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_class_creation(self):
        class_instance = ClassFactory()
        self.assertTrue(isinstance(class_instance, Class))
        self.assertEqual(
            str(class_instance),
            class_instance.class_id + ' - ' + class_instance.subject.initials)
        self.assertEqual(class_instance.positions, 30)
        self.assertEqual(class_instance.enrolled, 28)
        self.assertEqual(class_instance.subject.initials, "MC102")


class ScheduleModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_schedule_creation(self):
        schedule = ScheduleFactory()
        class_instance = ClassFactory()
        self.assertTrue(isinstance(schedule, Schedule))
        self.assertEqual(
            str(schedule), schedule.day + ": " + schedule.time_start + " - " +
            schedule.time_end)
        self.assertEqual(schedule.day, "Segunda")
        self.assertEqual(
            class_instance.schedules.get(place="CB01").place, "CB01")