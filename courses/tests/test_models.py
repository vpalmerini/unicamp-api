from django.test import TestCase
from courses.models import Course
from institutes.models import Institute


class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC",
            name="Instituto de Computação",
        )
        course = Course.objects.create(id=42,
                                       name="Ciência da Computação",
                                       institute=institute)


class CourseModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_course_creation(self):
        course = Course.objects.get(id=42)
        self.assertTrue(isinstance(course, Course))
        self.assertEqual(str(course), str(course.id) + " - " + course.name)
        self.assertEqual(course.institute.initials, "IC")
