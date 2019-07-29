from django.db import models
from institutes.models import Institute


class Subject(models.Model):
    # self properties
    initials = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=100)
    syllabus = models.TextField()
    year = models.CharField(max_length=4)
    workload = models.IntegerField()
    # relationships
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

    def __str__(self):
        return self.initials


class PreReq(models.Model):
    # self properties
    initials = models.CharField(max_length=200)
    year_start = models.CharField(max_length=4)
    year_end = models.CharField(max_length=4)

    # relationships
    subjects = models.ManyToManyField(Subject, related_name='prereqs')

    class Meta:
        verbose_name_plural = 'PreReqs'

    def __str__(self):
        return self.initials


class Continence(models.Model):
    # self properties
    initials = models.CharField(max_length=100)

    # relationships
    subjects = models.ManyToManyField(Subject, related_name='continences')

    def __str__(self):
        return self.initials


class Equivalence(models.Model):
    # self properties
    initials = models.CharField(max_length=200, primary_key=True)

    # relationships
    subjects = models.ManyToManyField(Subject, related_name='equivalences')

    def __str__(self):
        return self.initials
