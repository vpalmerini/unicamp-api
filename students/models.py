from django.db import models
from classes.models import Class
from courses.models import Course


class Student(models.Model):

    # self properties
    ra = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    # relationships
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    classes = models.ManyToManyField(Class, related_name='students')

    def save(self, *args, **kwargs):
        domain = "@dac.unicamp.br"
        if self.ra and self.name:
            self.email = self.name[0].lower() + self.ra + domain
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ra + ' - ' + self.name
