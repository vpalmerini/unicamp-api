from rest_framework import viewsets
from .models import Subject
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.permissions import IsSafeOrIsStaff


class SubjectViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsSafeOrIsStaff, )
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
