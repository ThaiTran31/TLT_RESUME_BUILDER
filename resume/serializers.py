from rest_framework import serializers

from .models import Resume
from resume_form.serializers import ComplexSectionSerializer, PersonalDetailsSerializer, ProfessionalSummarySerializer


class ResumeSerializer(serializers.ModelSerializer):
    complex_sections = ComplexSectionSerializer(many=True, read_only=True, required=False)
    personal_details = PersonalDetailsSerializer(many=False, read_only=True, required=False)
    professional_summary = ProfessionalSummarySerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "completeness",
            "template",
            "personal_details",
            "professional_summary",
            "complex_sections",
            "created_at",
            "updated_at",
            "layout",
            "image",
        ]


class ResumeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "thumbnail",
            "created_at",
            "updated_at",
        ]


class ImagesUploadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = [
            "image",
            "thumbnail",
        ]
