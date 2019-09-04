from django.test import TestCase
from courses.models import Course
from courses.serializers import CourseSerializer
from institutes.tests.factories import InstituteFactory


class CourseSerializerTest(TestCase):
    def setUp(self):
        institute = InstituteFactory()
        self.courses_attributes = {
            'id': 42,
            'name': 'Ciência da Computação',
            'shift': 'Noturno',
            'institute': institute
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
