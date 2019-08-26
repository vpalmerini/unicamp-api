from rest_framework import serializers
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    semesters = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='semester')
    prereqs = serializers.StringRelatedField(many=True, read_only=True)
    continences = serializers.StringRelatedField(many=True, read_only=True)
    equivalences = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'
