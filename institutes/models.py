from django.db import models


class Institute(models.Model):
    initials = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=100)

    def __str__(self):
        return self.initials
