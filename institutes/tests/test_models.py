from django.test import TestCase
from institutes.models import Institute
from institutes.tests.factories import InstituteFactory


class InstituteModelTest(TestCase):
    def setUp(self):
        pass

    def test_institute_creation(self):
        institute = InstituteFactory()
        self.assertTrue(isinstance(institute, Institute))
        self.assertEqual(str(institute), institute.initials)
        self.assertEqual(institute.name, "Instituto de Computação")
