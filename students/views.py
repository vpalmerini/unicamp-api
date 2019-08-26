from rest_framework import viewsets
from .models import Student
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.permissions import IsAuthenticatedOrIsStaff


class StudentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.StudentListSerializer
        return serializers.StudentDetailSerializer

    permission_classes = (IsAuthenticatedOrIsStaff, )
    queryset = Student.objects.all()