from rest_framework import viewsets
from .models import Course
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin


class CourseViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
