from rest_framework import viewsets
from .models import Subject
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin


class SubjectViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
