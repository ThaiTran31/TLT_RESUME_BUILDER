from rest_framework import serializers

from .models import ResumeTemplate


class ResumeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeTemplate
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
        ]
