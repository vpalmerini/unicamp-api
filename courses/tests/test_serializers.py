from django.test import TestCase
from courses.models import Course
from institutes.models import Institute
from courses.serializers import CourseSerializer


class CourseSerializerTest(TestCase):
    def setUp(self):
        institute1 = Institute(initials='IC', name='Instituto de Computação')
        institute1.save()
        self.courses_attributes = {
            'id': 42,
            'name': 'Ciência da Computação',
            'shift': 'Noturno',
            'institute': institute1
        }

        institute2 = Institute(
            initials='FEC',
            name='Faculdade de Engenharia Civil e Arquitetura e Urbanismo')
        institute2.save()
        self.serializer_data = {
            'id': 12,
            'name': 'Engenharia Civil',
            'shift': 'Integral',
            'institute': institute2
        }

        self.course = Course.objects.create(**self.courses_attributes)
        self.serializer = CourseSerializer(instance=self.course)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['id', 'name', 'shift', 'institute'])

    def test_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.courses_attributes['id'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.courses_attributes['name'])

    def test_shift_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['shift'], self.courses_attributes['shift'])

    def test_shift_must_be_in_choices(self):
        self.courses_attributes['shift'] = 'Afternoon'
        serializer = CourseSerializer(instance=self.course,
                                      data=self.courses_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['shift']))

    def test_institute_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['institute'],
                         self.courses_attributes['institute'].initials)
