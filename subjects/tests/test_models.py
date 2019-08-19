from django.test import TestCase
from subjects.models import Subject, Semester, PreReq, Continence, Equivalence
from institutes.models import Institute


class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC",
            name="Instituto de Computação",
        )
        semester = Semester.objects.create(semester=1, year="2019")
        subject = Subject.objects.create(
            initials="MC102",
            name="Algoritmos e Programação de Computadores",
            syllabus="""
                Conceitos básicos de organização de computadores. 
                Construção de algoritmos e sua representação em pseudocódigo e linguagens de alto nível. Desenvolvimento sistemático e implementação de programas. 
                Estruturação, depuração, testes e documentação de programas. 
                Resolução de problemas.
            """,
            workload=4,
            institute=institute)

        semester.subjects.add(subject)

        pre_req1 = PreReq.objects.create(initials="MC404 MC602",
                                         year_start="2014",
                                         year_end="2016")
        pre_req1.subjects.add(subject)

        pre_req2 = PreReq.objects.create(initials="EA772 MC404",
                                         year_start="2014",
                                         year_end="2016")
        pre_req2.subjects.add(subject)

        pre_req3 = PreReq.objects.create(initials="EA772 MC404",
                                         year_start="2017",
                                         year_end="2019")
        pre_req3.subjects.add(subject)

        continence = Continence.objects.create(initials="AL003")
        continence.subjects.add(subject)

        equivalence = Equivalence.objects.create(initials="EA869")
        equivalence.subjects.add(subject)


class SubjectModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_subject_creation(self):
        subject = Subject.objects.get(initials="MC102")
        pre_req = PreReq.objects.get(initials="MC404 MC602")
        self.assertTrue(isinstance(subject, Subject))
        self.assertEqual(str(subject), subject.initials)
        self.assertEqual(subject.name,
                         "Algoritmos e Programação de Computadores")
        self.assertEqual(subject.workload, 4)
        self.assertEqual(subject.institute.initials, "IC")
        self.assertEqual(pre_req.subjects.get(initials="MC102").workload, 4)
