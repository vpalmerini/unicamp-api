from django.db import models

class Institute(models.Model):
    initials = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=100)

    def __str__(self):
        return self.initials


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


class Class(models.Model):
    # self properties
    class_id = models.CharField(max_length=5)
    positions = models.IntegerField()
    enrolled = models.IntegerField()
    # relationships
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_id


class Course(models.Model):
    # self properties
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    # relationships
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.name


class Schedule(models.Model):
    # self properties
    day = models.CharField(max_length=10)
    time_start = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    place = models.CharField(max_length=20)
    # relationships
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.day + ': ' + self.time_start + ' - ' + self.time_end


class Professor(models.Model):
    # self properties
    name = models.CharField(max_length=100)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    web_page = models.URLField(blank=True)
    # relationships
    classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.name


class PreReq(models.Model):
    # self properties
    initials = models.CharField(max_length=10)
    year_start = models.CharField(max_length=4)
    year_end = models.CharField(max_length=4)
    # relationships
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.initials


class Continence(models.Model):
    # self properties
    initials = models.CharField(max_length=10)
    # relationships
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.initials


class Equivalence(models.Model):
    # self properties
    initials = models.CharField(max_length=10)
    # relationships
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.initials