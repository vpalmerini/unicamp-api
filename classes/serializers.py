from rest_framework import serializers
from .models import Class
from students.serializers import StudentListSerializer


class ClassListSerializer(serializers.ModelSerializer):
    schedules = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Class
        fields = [
            'class_id', 'positions', 'enrolled', 'subject',
            'course_reservation', 'schedules', 'professors'
        ]


class ClassDetailSerializer(serializers.ModelSerializer):
    schedules = serializers.StringRelatedField(many=True, read_only=True)
    students = StudentListSerializer(many=True, read_only=True)
    professors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Class
        fields = [
            'class_id', 'positions', 'enrolled', 'subject',
            'course_reservation', 'schedules', 'professors', 'students'
        ]


class ClassListStudenDetailSerializer(serializers.ModelSerializer):
    """
    Serializes fields to show in student-detail endpoint
    """
    schedules = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['class_id', 'subject', 'schedules', 'professors']
