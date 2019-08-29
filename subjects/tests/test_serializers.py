from django.test import TestCase
from subjects.models import Subject, Semester, PreReq, Continence, Equivalence
from institutes.models import Institute
from subjects.serializers import SubjectSerializer


class SubjectSerializerTest(TestCase):
    def setUp(self):
        institute = Institute(initials='IC', name='Instituto de Computação')
        institute.save()
        semester = Semester(semester=1, year='2019')
        semester.save()
        pre_req = PreReq(id=1,
                         initials='MC102',
                         year_start='2000',
                         year_end='2019')
        pre_req.save()
        continence = Continence(initials='MC002')
        continence.save()
        equivalence = Equivalence(initials='MC100')
        equivalence.save()

        self.subject_attributes = {
            'initials': 'MC202',
            'name': 'Estrutura de Dados',
            'syllabus': 'Listas Ligadas e Árvores',
            'workload': 6,
            'institute': institute,
        }

        self.subject = Subject.objects.create(**self.subject_attributes)
        self.subject_attributes['semesters'] = semester
        self.subject_attributes['prereqs'] = pre_req
        self.subject_attributes['continences'] = continence
        self.subject_attributes['equivalences'] = equivalence
        semester.subjects.add(self.subject)
        pre_req.subjects.add(self.subject)
        continence.subjects.add(self.subject)
        equivalence.subjects.add(self.subject)

        self.serializer = SubjectSerializer(instance=self.subject)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), [
            'initials', 'name', 'syllabus', 'workload', 'institute',
            'semesters', 'prereqs', 'continences', 'equivalences'
        ])

    def test_initials_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['initials'], self.subject_attributes['initials'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.subject_attributes['name'])

    def test_syllabus_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['syllabus'], self.subject_attributes['syllabus'])

    def test_workload_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['workload'], self.subject_attributes['workload'])

    def test_institute_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['institute'],
                         self.subject_attributes['institute'].initials)

    def test_semester_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['semesters'].pop(),
                         self.subject_attributes['semesters'].semester)

    def test_prereq_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['prereqs'].pop(),
                         self.subject_attributes['prereqs'].initials)

    def test_continences_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['continences'].pop(),
                         self.subject_attributes['continences'].initials)

    def test_equivalences_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['equivalences'].pop(),
                         self.subject_attributes['equivalences'].initials)
