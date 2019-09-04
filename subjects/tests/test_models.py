from django.test import TestCase
from subjects.models import Subject, Semester, PreReq, Continence, Equivalence
from subjects.tests.factories import SemesterFactory, SubjectFactory, PreReqFactory, ContinenceFactory, EquivalenceFactory


class BaseModelTest(TestCase):
    def setUp(self):
        semester = SemesterFactory()
        subject = SubjectFactory()

        semester.subjects.add(subject)

        pre_req = PreReqFactory()
        pre_req.subjects.add(subject)

        continence = ContinenceFactory()
        continence.subjects.add(subject)

        equivalence = EquivalenceFactory()
        equivalence.subjects.add(subject)


class SubjectModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_subject_creation(self):
        subject = SubjectFactory()
        pre_req = PreReqFactory()
        self.assertTrue(isinstance(subject, Subject))
        self.assertEqual(str(subject), subject.initials)
        self.assertEqual(subject.name,
                         "Algoritmos e Programação de Computadores")
        self.assertEqual(subject.workload, 6)
        self.assertEqual(subject.institute.initials, "IC")
        self.assertEqual(pre_req.subjects.get(initials="MC102").workload, 6)
