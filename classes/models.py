from django.db import models
from subjects.models import Subject
from courses.models import Course


class Class(models.Model):
    # self properties
    class_id = models.CharField(max_length=10)
    positions = models.IntegerField()
    enrolled = models.IntegerField()
    # relationships
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course_reservation = models.ManyToManyField(Course, related_name='courses')

    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['subject']

    def __str__(self):
        return self.class_id + ' - ' + self.subject.initials


class Schedule(models.Model):
    # self properties
    day = models.CharField(max_length=10)
    time_start = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    place = models.CharField(max_length=20)
    # relationships
    class_id = models.ForeignKey(Class,
                                 related_name='schedules',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.day + ': ' + self.time_start + ' - ' + self.time_end
