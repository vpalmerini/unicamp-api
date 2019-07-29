from rest_framework import viewsets
from .models import Institute
from . import serializers


class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = serializers.InstituteSerializer
