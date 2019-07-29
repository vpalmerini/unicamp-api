from django.db import models
from institutes.models import Institute


class Course(models.Model):
    # self properties
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    SHIFT_CHOICES = [("Integral", "Integral"), ("Noturno", "Noturno")]
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    # relationships
    institute = models.ForeignKey(Institute,
                                  on_delete=models.CASCADE,
                                  related_name='courses')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id) + ' - ' + self.name


class Specialization(models.Model):
    # self properties
    code = models.CharField(max_length=10)
    specialization = models.CharField(max_length=100)
    # relationships
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.code + ' - ' + self.specialization
