from rest_framework import viewsets
from .models import Subject
from . import serializers


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
