from rest_framework import viewsets
from .models import Professor
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin


class ProfessorViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = serializers.ProfessorSerializer
