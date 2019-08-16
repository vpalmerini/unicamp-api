from rest_framework import viewsets
from .models import Class
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin


class ClassViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = serializers.ClassSerializer
    lookup_field = 'class_id'