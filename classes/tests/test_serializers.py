from django.test import TestCase
from classes.models import Class
from classes.serializers import ClassListSerializer, ClassDetailSerializer, ClassListStudenDetailSerializer
from subjects.tests.factories import SemesterFactory, PreReqFactory, ContinenceFactory, EquivalenceFactory, SubjectFactory
from courses.tests.factories import CourseFactory
from classes.tests.factories import ScheduleFactory
from professors.tests.factories import ProfessorFactory
from students.tests.factories import StudentFactory


class ClassSerializerBaseTest(TestCase):
    def setUp(self):
        semester = SemesterFactory()
        pre_req = PreReqFactory()
        continence = ContinenceFactory()
        equivalence = EquivalenceFactory()
        subject = SubjectFactory()
        semester.subjects.add(subject)
        pre_req.subjects.add(subject)
        continence.subjects.add(subject)
        equivalence.subjects.add(subject)

        self.class_attributes = {
            'class_id': 'A',
            'positions': 30,
            'enrolled': 28,
            'subject': subject
        }
        self._class = Class.objects.create(**self.class_attributes)

        course = CourseFactory()
        schedule = ScheduleFactory()
        professor = ProfessorFactory()

        self.class_attributes['schedules'] = schedule
        self.class_attributes['course'] = course
        self.class_attributes['professors'] = professor
        course.classes.add(self._class)
        professor.classes.add(self._class)


class ClassListSerializerTest(ClassSerializerBaseTest):
    def setUp(self):
        ClassSerializerBaseTest.setUp(self)
        self.serializer = ClassListSerializer(instance=self._class)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), [
            'class_id', 'positions', 'enrolled', 'subject',
            'course_reservation', 'schedules', 'professors'
        ])

    def test_class_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['class_id'], self.class_attributes['class_id'])

    def test_positions_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['positions'], self.class_attributes['positions'])

    def test_enrolled_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['enrolled'], self.class_attributes['enrolled'])

    def test_subject_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['subject'],
                         self.class_attributes['subject'].initials)

    def test_schedules_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['schedules'].pop(),
                         str(self.class_attributes['schedules']))

    def test_professors_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['professors'].pop(),
                         self.class_attributes['professors'].name)


class ClassDetailSerializerTest(ClassListSerializerTest):
    def setUp(self):
        ClassListSerializerTest.setUp(self)
        student = StudentFactory()
        student.classes.add(self._class)
        self.class_attributes['students'] = student
        self.serializer = ClassDetailSerializer(instance=self._class)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), [
            'class_id', 'positions', 'enrolled', 'subject',
            'course_reservation', 'schedules', 'professors', 'students'
        ])

    def test_class_id_field_content(self):
        ClassListSerializerTest.test_class_id_field_content(self)

    def test_positions_field_content(self):
        ClassListSerializerTest.test_positions_field_content(self)

    def test_enrolled_field_content(self):
        ClassListSerializerTest.test_enrolled_field_content(self)

    def test_subject_field_content(self):
        ClassListSerializerTest.test_subject_field_content(self)

    def test_schedules_field_content(self):
        ClassListSerializerTest.test_schedules_field_content(self)

    def test_professors_field_content(self):
        ClassListSerializerTest.test_professors_field_content(self)

    def test_students_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['students'].pop()['ra'],
                         self.class_attributes['students'].ra)


class ClassListStudentDetailSerializerTest(ClassSerializerBaseTest):
    def setUp(self):
        ClassSerializerBaseTest.setUp(self)
        self.serializer = ClassListStudenDetailSerializer(instance=self._class)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ['class_id', 'subject', 'schedules', 'professors'])

    def test_class_id_field_content(self):
        ClassListSerializerTest.test_class_id_field_content(self)

    def test_subject_field_content(self):
        ClassListSerializerTest.test_subject_field_content(self)

    def test_schedules_field_content(self):
        ClassListSerializerTest.test_schedules_field_content(self)

    def test_professors_field_content(self):
        ClassListSerializerTest.test_professors_field_content(self)
