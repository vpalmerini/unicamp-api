from django.test import TestCase
from professors.models import Professor
from professors.serializers import ProfessorSerializer
from institutes.tests.factories import InstituteFactory
from subjects.tests.factories import SemesterFactory, SubjectFactory, PreReqFactory, ContinenceFactory, EquivalenceFactory
from classes.tests.factories import ClassFactory


class ProfessorSerializerTest(TestCase):
    def setUp(self):
        institute = InstituteFactory()
        semester = SemesterFactory()
        pre_req = PreReqFactory()
        continence = ContinenceFactory()
        equivalence = EquivalenceFactory()
        subject = SubjectFactory()
        semester.subjects.add(subject)
        pre_req.subjects.add(subject)
        continence.subjects.add(subject)
        equivalence.subjects.add(subject)

        _class = ClassFactory()

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
