from django.test import TestCase
from students.models import Student
from institutes.models import Institute
from courses.models import Course
from classes.models import Class
from subjects.models import Subject, Semester


class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC",
            name="Instituto de Computação",
        )
        course = Course.objects.create(id=42,
                                       name="Ciência da Computação",
                                       institute=institute)
        student = Student.objects.create(ra="178061",
                                         name="Victor Palmerini",
                                         course=course)
        semester = Semester.objects.create(semester=1, year="2019")
        subject = Subject.objects.create(
            initials="MC102",
            name="Algoritmos e Programação de Computadores",
            syllabus="""
                Conceitos básicos de organização de computadores. 
                Construção de algoritmos e sua representação em pseudocódigo e linguagens de alto nível. Desenvolvimento sistemático e implementação de programas. 
                Estruturação, depuração, testes e documentação de programas. 
                Resolução de problemas.
            """,
            workload=4,
            institute=institute)

        semester.subjects.add(subject)
        class_instance1 = Class.objects.create(class_id="A",
                                               positions=30,
                                               enrolled=25,
                                               subject=subject)
        class_instance2 = Class.objects.create(class_id="B",
                                               positions=28,
                                               enrolled=26,
                                               subject=subject)
        student.classes.add(class_instance1)
        student.classes.add(class_instance2)


class StudentModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_student_creation(self):
        student_instance = Student.objects.get(ra="178061")
        self.assertTrue(isinstance(student_instance, Student))
        self.assertEqual(str(student_instance),
                         student_instance.ra + ' - ' + student_instance.name)
        self.assertEqual(student_instance.email, "v178061@dac.unicamp.br")
        self.assertEqual(len(student_instance.classes.all()), 2)
        self.assertEquals(student_instance.course.id, 42)
