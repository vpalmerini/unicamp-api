from rest_framework import viewsets
from .models import Student
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin


class StudentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
