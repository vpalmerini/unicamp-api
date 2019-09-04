from django.test import TestCase
from students.models import Student
from students.tests.factories import StudentFactory
from subjects.tests.factories import SemesterFactory, SubjectFactory
from classes.tests.factories import ClassFactory


class BaseModelTest(TestCase):
    def setUp(self):
        student = StudentFactory()
        semester = SemesterFactory()
        subject = SubjectFactory()

        semester.subjects.add(subject)
        class_instance = ClassFactory()
        student.classes.add(class_instance)


class StudentModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_student_creation(self):
        student_instance = StudentFactory()
        self.assertTrue(isinstance(student_instance, Student))
        self.assertEqual(str(student_instance),
                         student_instance.ra + ' - ' + student_instance.name)
        self.assertEqual(student_instance.email, "v100000@dac.unicamp.br")
        self.assertEqual(len(student_instance.classes.all()), 1)
        self.assertEquals(student_instance.course.id, 42)
