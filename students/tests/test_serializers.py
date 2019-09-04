from django.test import TestCase
from students.models import Student
from students.serializers import StudentListSerializer, StudentDetailSerializer
from courses.tests.factories import CourseFactory
from subjects.tests.factories import SemesterFactory, PreReqFactory, ContinenceFactory, EquivalenceFactory, SubjectFactory
from classes.tests.factories import ClassFactory


class StudentSerializerBaseTest(TestCase):
    def setUp(self):
        course = CourseFactory()
        semester = SemesterFactory()
        pre_req = PreReqFactory()
        continence = ContinenceFactory()
        equivalence = EquivalenceFactory()
        subject = SubjectFactory()

        semester.subjects.add(subject)
        pre_req.subjects.add(subject)
        continence.subjects.add(subject)
        equivalence.subjects.add(subject)

        self.student_attributes = {
            'ra': '100000',
            'name': 'Victor Palmerini',
            'email': 'v100000@dac.unicamp.br',
            'course': course
        }

        self.student = Student.objects.create(**self.student_attributes)


class StudentListSerializerTest(StudentSerializerBaseTest):
    def setUp(self):
        StudentSerializerBaseTest.setUp(self)
        self.serializer = StudentListSerializer(instance=self.student)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['ra', 'name', 'email', 'course'])

    def test_ra_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['ra'], self.student_attributes['ra'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.student_attributes['name'])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.student_attributes['email'])

    def test_course_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['course'], self.student_attributes['course'].id)


class StudentDetailSerializerTest(StudentListSerializerTest):
    def setUp(self):
        StudentListSerializerTest.setUp(self)
        subject = SubjectFactory()
        _class = ClassFactory()
        _class.students.add(self.student)
        self.student_attributes['classes'] = _class
        self.serializer = StudentDetailSerializer(instance=self.student)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(),
                              ['ra', 'name', 'email', 'course', 'classes'])

    def test_ra_field_content(self):
        StudentListSerializerTest.test_ra_field_content(self)

    def test_name_field_content(self):
        StudentListSerializerTest.test_name_field_content(self)

    def test_email_field_content(self):
        StudentListSerializerTest.test_email_field_content(self)

    def test_course_field_content(self):
        StudentListSerializerTest.test_course_field_content(self)

    def test_classes_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['classes'].pop()['class_id'],
                         self.student_attributes['classes'].class_id)