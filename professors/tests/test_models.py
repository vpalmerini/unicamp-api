from django.test import TestCase
from professors.models import Professor
from institutes.models import Institute


class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC",
            name="Instituto de Computação",
        )
        professor = Professor.objects.create(
            name="Pedro Rezende",
            institute=institute,
            web_page="http://www.ic.unicamp.br/~rezende/",
        )

    def test_professor_creation(self):
        professor = Professor.objects.get(name="Pedro Rezende")
        self.assertTrue(isinstance(professor, Professor))
        self.assertEqual(professor.name, "Pedro Rezende")
        self.assertEqual(professor.web_page,
                         "http://www.ic.unicamp.br/~rezende/")
        self.assertEqual(professor.institute.initials, "IC")
