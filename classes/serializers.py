from rest_framework import serializers
from .models import Class
from students.serializers import StudentSerializer


class ClassSerializer(serializers.ModelSerializer):
    schedules = serializers.StringRelatedField(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    professors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Class
        fields = [
            'class_id', 'positions', 'enrolled', 'subject',
            'course_reservation', 'schedules', 'professors', 'students'
        ]


class ClassListSerializer(ClassSerializer):
    class Meta:
        model = Class
        fields = [
            'class_id', 'positions', 'enrolled', 'subject',
            'course_reservation', 'schedules', 'professors'
        ]
