from rest_framework import viewsets
from .models import Class
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.permissions import IsSafeOrIsStaff


class ClassViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ClassListSerializer
        return serializers.ClassSerializer

    permission_classes = (IsSafeOrIsStaff, )
    queryset = Class.objects.all()
    lookup_field = 'class_id'