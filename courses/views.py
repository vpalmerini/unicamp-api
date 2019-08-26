from rest_framework import viewsets
from .models import Course
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.permissions import IsSafeOrIsStaff


class CourseViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsSafeOrIsStaff, )
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
