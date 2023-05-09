from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import JobPosting


@registry.register_document
class JobPostingDocument(Document):
    class Index:
        name = "job_posting"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = JobPosting
        fields = [
            "id",
            "job_portal",
            "job_title",
            "company",
            "date",
            "link",
            "location",
            "details",
            "searching_location"
        ]
