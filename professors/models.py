from django.db import models
from institutes.models import Institute
from classes.models import Class


class Professor(models.Model):
    # self properties
    name = models.CharField(max_length=100, primary_key=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    web_page = models.URLField(blank=True)
    # relationships
    classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.name
