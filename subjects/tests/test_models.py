from django.test import TestCase
from subjects.models import *

class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC", 
            name="Instituto de Computação", 
            link="https://www.dac.unicamp.br/portal/caderno-de-horarios/2019/1/S/G/IC"
        )
        subject = Subject.objects.create(
            initials="MC102",
            name="Algoritmos e Programação de Computadores",
            link="https://www.dac.unicamp.br/portal/caderno-de-horarios/2019/1/S/G/IC/MC102",
            syllabus="""
                Conceitos básicos de organização de computadores. 
                Construção de algoritmos e sua representação em pseudocódigo e linguagens de alto nível. Desenvolvimento sistemático e implementação de programas. 
                Estruturação, depuração, testes e documentação de programas. 
                Resolução de problemas.
            """,
            year='2019',
            workload=4,
            institute=institute
        )
        class_instance1 = Class.objects.create(
            class_id='A',
            positions=30,
            enrolled=25,
            subject=subject
        )
        class_instance2 = Class.objects.create(
            class_id='B',
            positions=28,
            enrolled=26,
            subject=subject
        )
        course = Course.objects.create(
            id=42,
            name='Ciência da Computação',
            institute=institute
        )
        schedule1 = Schedule.objects.create(
            day='Segunda',
            time_start='10:00',
            time_end='12:00',
            place='CB01',
            class_id=class_instance1
        )
        schedule2 = Schedule.objects.create(
            day='Quarta',
            time_start='14:00',
            time_end='16:00',
            place='CB02',
            class_id=class_instance1
        )
        schedule3 = Schedule.objects.create(
            day='Terça',
            time_start='14:00',
            time_end='16:00',
            place='CB03',
            class_id=class_instance2
        )
        schedule4 = Schedule.objects.create(
            day='Quinta',
            time_start='14:00',
            time_end='16:00',
            place='CB04',
            class_id=class_instance2
        )
        professor = Professor.objects.create(
            name='Pedro Rezende',
            institute=institute,
            web_page='http://www.ic.unicamp.br/~rezende/',
        )
        professor.classes.add(class_instance1)
        professor.classes.add(class_instance2)

        pre_req1 = PreReq.objects.create(
            initials="MC404 MC602",
            year_start="2014",
            year_end="2016"
        )
        pre_req1.subjects.add(subject)

        pre_req2 = PreReq.objects.create(
            initials="EA772 MC404",
            year_start="2014",
            year_end="2016"
        )
        pre_req2.subjects.add(subject)

        pre_req3 = PreReq.objects.create(
            initials="EA772 MC404",
            year_start="2017",
            year_end="2019"
        )
        pre_req3.subjects.add(subject)

        continence = Continence.objects.create(
            initials="AL003"
        )
        continence.subjects.add(subject)

        equivalence = Equivalence.objects.create(
            initials="EA869"
        )
        equivalence.subjects.add(subject)


class InstituteModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_institute_creation(self):
        institute = Institute.objects.get(initials="IC")
        self.assertTrue(isinstance(institute, Institute))
        self.assertEqual(str(institute), institute.initials)
        self.assertEqual(institute.name, 'Instituto de Computação')
        self.assertEqual(institute.link, 'https://www.dac.unicamp.br/portal/caderno-de-horarios/2019/1/S/G/IC')



class SubjectModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)
    
    def test_subject_creation(self):
        subject = Subject.objects.get(initials="MC102")
        pre_req = PreReq.objects.get(initials="MC404 MC602")
        self.assertTrue(isinstance(subject, Subject))
        self.assertEqual(str(subject), subject.initials)
        self.assertEqual(subject.name, 'Algoritmos e Programação de Computadores')
        self.assertEqual(subject.link, 'https://www.dac.unicamp.br/portal/caderno-de-horarios/2019/1/S/G/IC/MC102')
        self.assertEqual(subject.year, '2019')
        self.assertEqual(subject.workload, 4)
        self.assertEqual(subject.institute.initials, "IC")
        self.assertEqual(pre_req.subjects.get(initials="MC102").workload, 4)


class ClassModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_class_creation(self):
        class_instance = Class.objects.get(class_id='A')
        self.assertTrue(isinstance(class_instance, Class))
        self.assertEqual(str(class_instance), class_instance.class_id)
        self.assertEqual(class_instance.positions, 30)
        self.assertEqual(class_instance.enrolled, 25)
        self.assertEqual(class_instance.subject.initials, "MC102")


class CourseModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_course_creation(self):
        course = Course.objects.get(id=42)
        self.assertTrue(isinstance(course, Course))
        self.assertEqual(str(course), str(course.id) + ' - ' + course.name)
        self.assertEqual(course.institute.initials, "IC")


class ScheduleModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_schedule_creation(self):
        schedule = Schedule.objects.get(place="CB01")
        class_instance = Class.objects.get(class_id="A")
        self.assertTrue(isinstance(schedule, Schedule))
        self.assertEqual(str(schedule), schedule.day + ': ' + schedule.time_start + ' - ' + schedule.time_end)
        self.assertEqual(schedule.day, "Segunda")
        self.assertEqual(class_instance.schedule_set.get(place="CB01").place, "CB01")

class ProfessorModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_professor_creation(self):
        professor = Professor.objects.get(id=1)
        class_instance = Class.objects.get(class_id="A")
        self.assertTrue(isinstance(professor, Professor))
        self.assertEqual(professor.name, "Pedro Rezende")
        self.assertEqual(professor.web_page, "http://www.ic.unicamp.br/~rezende/")
        self.assertEqual(professor.institute.initials, "IC")
        self.assertEqual(class_instance.professor_set.get(id=1).name, "Pedro Rezende")