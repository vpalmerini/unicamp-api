from django.test import TestCase
from courses.models import Course
from institutes.models import Institute
from courses.tests.factories import CourseFactory


class CourseModelTest(TestCase):
    def setUp(self):
        pass

    def test_course_creation(self):
        course = CourseFactory()
        self.assertTrue(isinstance(course, Course))
        self.assertEqual(str(course), str(course.id) + " - " + course.name)
        self.assertEqual(course.institute.initials, "IC")
