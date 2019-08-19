from django.test import TestCase
from institutes.models import Institute


class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC",
            name="Instituto de Computação",
        )


class InstituteModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_institute_creation(self):
        institute = Institute.objects.get(initials="IC")
        self.assertTrue(isinstance(institute, Institute))
        self.assertEqual(str(institute), institute.initials)
        self.assertEqual(institute.name, "Instituto de Computação")
