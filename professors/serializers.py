from rest_framework import serializers
from .models import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    classes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Professor
        fields = '__all__'