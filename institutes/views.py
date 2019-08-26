from rest_framework import viewsets
from .models import Institute
from . import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.permissions import IsSafeOrIsStaff


class InstituteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsSafeOrIsStaff, )
    queryset = Institute.objects.all()
    serializer_class = serializers.InstituteSerializer
