from django.test import TestCase
from classes.models import Class, Schedule
from institutes.models import Institute
from subjects.models import Subject, Semester


class BaseModelTest(TestCase):
    def setUp(self):
        institute = Institute.objects.create(
            initials="IC",
            name="Instituto de Computação",
        )
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
        schedule1 = Schedule.objects.create(day="Segunda",
                                            time_start="10:00",
                                            time_end="12:00",
                                            place="CB01",
                                            class_id=class_instance1)
        schedule2 = Schedule.objects.create(day="Quarta",
                                            time_start="14:00",
                                            time_end="16:00",
                                            place="CB02",
                                            class_id=class_instance1)
        schedule3 = Schedule.objects.create(day="Terça",
                                            time_start="14:00",
                                            time_end="16:00",
                                            place="CB03",
                                            class_id=class_instance2)
        schedule4 = Schedule.objects.create(day="Quinta",
                                            time_start="14:00",
                                            time_end="16:00",
                                            place="CB04",
                                            class_id=class_instance2)


class ClassModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_class_creation(self):
        class_instance = Class.objects.get(class_id="A")
        self.assertTrue(isinstance(class_instance, Class))
        self.assertEqual(
            str(class_instance),
            class_instance.class_id + ' - ' + class_instance.subject.initials)
        self.assertEqual(class_instance.positions, 30)
        self.assertEqual(class_instance.enrolled, 25)
        self.assertEqual(class_instance.subject.initials, "MC102")


class ScheduleModelTest(BaseModelTest):
    def setUp(self):
        BaseModelTest.setUp(self)

    def test_schedule_creation(self):
        schedule = Schedule.objects.get(place="CB01")
        class_instance = Class.objects.get(class_id="A")
        self.assertTrue(isinstance(schedule, Schedule))
        self.assertEqual(
            str(schedule), schedule.day + ": " + schedule.time_start + " - " +
            schedule.time_end)
        self.assertEqual(schedule.day, "Segunda")
        self.assertEqual(
            class_instance.schedules.get(place="CB01").place, "CB01")