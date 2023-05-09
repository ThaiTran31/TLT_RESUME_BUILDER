from dataclasses import field
from email import header
from rest_framework import serializers

from .models import PersonalDetails, ProfessionalSummary, ComplexSection, EmploymentHistory, Education, Custom, Skill, Link


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = [
            "id",
            "header",
            "position",
            "first_name",
            "last_name",
            "job_title",
            "address",
            "country",
            "city",
            "nationality",
            "email",
            "place_of_birth",
            "date_of_birth",
            "phone",
            "photo",
        ]


class ProfessionalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalSummary
        fields = [
            "id",
            "header",
            "position",
            "content",
        ]


class EmploymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentHistory
        fields = [
            "id",
            "position",
            "job_title",
            "employer",
            "description",
            "city",
            "start_date",
            "end_date",
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "position",
            "school",
            "degree",
            "description",
            "city",
            "start_date",
            "end_date",
        ]


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = [
            "id",
            "position",
            "title",
            "description",
            "city",
            "start_date",
            "end_date",
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "position",
            "name",
            "level",
        ]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "id",
            "position",
            "label",
            "link",
        ]


class ComplexSectionSerializer(serializers.ModelSerializer):
    employment_histories = EmploymentHistorySerializer(many=True, required=False, read_only=True)
    educations = EducationSerializer(many=True, required=False, read_only=True)
    skills = SkillSerializer(many=True, required=False, read_only=True)
    links = LinkSerializer(many=True, required=False, read_only=True)
    customs = CustomSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = ComplexSection
        fields = [
            "id",
            "header",
            "position",
            "section_type",
            "employment_histories",
            "educations",
            "skills",
            "links",
            "customs",
        ]
