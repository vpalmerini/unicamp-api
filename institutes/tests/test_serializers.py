from django.test import TestCase
from institutes.models import Institute
from institutes.serializers import InstituteSerializer


class InstituteSerializerTest(TestCase):
    def setUp(self):
        self.institute_attributes = {
            'initials': 'IC',
            'name': 'Instituto de Computação'
        }

        self.serializer_data = {
            'initials': 'FEEC',
            'name': 'Faculdade de Engenharia Elétrica e Computação'
        }

        self.institute = Institute.objects.create(**self.institute_attributes)
        self.serializer = InstituteSerializer(instance=self.institute)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['initials', 'name'])

    def test_initials_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['initials'],
                         self.institute_attributes['initials'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.institute_attributes['name'])
