from django.test import TestCase
from students.models import Student
from institutes.models import Institute
from courses.models import Course
from subjects.models import Subject, Semester, PreReq, Continence, Equivalence
from classes.models import Class
from students.serializers import StudentListSerializer


class StudentSerializerBaseTest(TestCase):
    def setUp(self):
        institute = Institute(initials='IC', name='Instituto de Computação')
        institute.save()
        course = Course(id=42,
                        name='Ciência da Computação',
                        shift='Noturno',
                        institute=institute)
        course.save()
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
