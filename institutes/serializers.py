from rest_framework import serializers
from .models import Institute


class InstituteSerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Institute
        fields = '__all__'
