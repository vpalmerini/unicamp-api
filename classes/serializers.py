from rest_framework import serializers
from .models import Class


class ClassSerializer(serializers.ModelSerializer):
    schedules = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Class
        fields = '__all__'
