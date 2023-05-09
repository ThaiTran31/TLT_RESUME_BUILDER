from rest_framework import serializers

from .models import JobPosting


class JobPostingSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPosting
        fields = [
            "job_portal",
            "job_title",
            "company",
            "date",
            "link",
            "location",
            "details",
            "searching_location",
        ]
