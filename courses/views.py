from rest_framework import viewsets
from .models import Course
from . import serializers


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer