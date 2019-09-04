from django.test import TestCase
from professors.models import Professor
from professors.tests.factories import ProfessorFactory


class ProfessorModelTest(TestCase):
    def setUp(self):
        pass

    def test_professor_creation(self):
        professor = ProfessorFactory()
        self.assertTrue(isinstance(professor, Professor))
        self.assertEqual(professor.name, "Pedro Rezende")
        self.assertEqual(professor.web_page,
                         "https://www.ic.unicamp.br/~rezende/")
        self.assertEqual(professor.institute.initials, "IC")
