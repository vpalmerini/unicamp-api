from rest_framework import viewsets
from .models import Professor
from . import serializers


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = serializers.ProfessorSerializer
