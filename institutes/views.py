from rest_framework import viewsets
from .models import Institute
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin


class InstituteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = serializers.InstituteSerializer
