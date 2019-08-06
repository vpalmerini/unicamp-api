from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    prereqs = serializers.StringRelatedField(many=True, read_only=True)
    continences = serializers.StringRelatedField(many=True, read_only=True)
    equivalences = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'
