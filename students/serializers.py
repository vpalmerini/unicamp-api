from rest_framework import serializers
from .models import Student


class StudentDetailSerializer(serializers.ModelSerializer):
    classes = serializers.SerializerMethodField()

    def get_classes(self, obj):
        from classes.serializers import ClassListSerializer
        return ClassListSerializer(obj.classes, many=True, read_only=True).data

    class Meta:
        model = Student
        fields = ('ra', 'name', 'email', 'course', 'classes')


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('ra', 'name', 'email', 'course')