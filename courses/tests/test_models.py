from django.test import TestCase
from courses.models import Course, Specialization
from institutes.models import Institute
from courses.tests.factories import CourseFactory, SpecializationFactory


class CourseModelTest(TestCase):
    def setUp(self):
        pass

    def test_course_creation(self):
        course = CourseFactory()
        self.assertTrue(isinstance(course, Course))
        self.assertEqual(str(course), str(course.id) + " - " + course.name)
        self.assertEqual(course.institute.initials, "IC")


class SpecializationTest(TestCase):
    def setUp(self):
        pass

    def test_specialization_creation(self):
        course = CourseFactory()
        specialization = SpecializationFactory()
        self.assertTrue(isinstance(specialization, Specialization))
        self.assertEqual(
            str(specialization),
            str(specialization.code) + ' - ' +
            str(specialization.specialization))

        self.assertEqual(specialization.code, "AB")
