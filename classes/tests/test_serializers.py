from django.test import TestCase
from classes.models import Class, Schedule
from institutes.models import Institute
from courses.models import Course
from subjects.models import Subject, Semester, Continence, Equivalence, PreReq
from professors.models import Professor
from students.models import Student
from classes.serializers import ClassListSerializer, ClassDetailSerializer, ClassListStudenDetailSerializer


class ClassSerializerBaseTest(TestCase):
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

        self.class_attributes = {
            'class_id': 'A',
            'positions': 30,
            'enrolled': 28,
            'subject': subject
        }
        self._class = Class.objects.create(**self.class_attributes)

        course = Course(id=42,
                        name='Ciência da Computação',
                        shift='Noturno',
                        institute=institute)
        course.save()
        schedule = Schedule(day='Segunda',
                            time_start='14:00',
                            time_end='16:00',
                            place='CB02',
                            class_id=self._class)
        schedule.save()
        professor = Professor(name='Pedro Rezende', institute=institute)
        professor.save()

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
        course = Course.objects.get()
        student = Student(ra='100000', name='Victor Palmerini', course=course)
        student.save()
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
