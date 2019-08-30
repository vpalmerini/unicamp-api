from django.test import TestCase
from professors.models import Professor
from institutes.models import Institute
from subjects.models import Subject, Semester, PreReq, Continence, Equivalence
from classes.models import Class
from professors.serializers import ProfessorSerializer


class ProfessorSerializerTest(TestCase):
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
        subject = Subject(initials='MC202',
                          name='Estrutura de Dados',
                          syllabus='Listas Ligadas e Árvores',
                          workload=6,
                          institute=institute)
        subject.save()
        semester.subjects.add(subject)
        pre_req.subjects.add(subject)
        continence.subjects.add(subject)
        equivalence.subjects.add(subject)

        _class = Class(id=1,
                       class_id='A',
                       positions=30,
                       enrolled=28,
                       subject=subject)
        _class.save()

        self.professor_attributes = {
            'name': 'Pedro Rezende',
            'web_page': 'https://www.unicamp.com.br/pedro_rezende',
            'institute': institute
        }
        self.professor = Professor.objects.create(**self.professor_attributes)
        _class.professors.add(self.professor)
        self.professor_attributes['classes'] = _class
        self.serializer = ProfessorSerializer(instance=self.professor)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['name', 'web_page', 'institute', 'classes'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.professor_attributes['name'])

    def test_web_page_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['web_page'],
                         self.professor_attributes['web_page'])

    def test_institute_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['institute'],
                         self.professor_attributes['institute'].initials)

    def test_classes_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['classes'].pop(),
                         self.professor_attributes['classes'].id)
