from django.db import models


class JobPosting(models.Model):
    SOURCE_CHOICES = [
        ('linkedin', 'Linkedin'),
        ('vietnamworks', 'Vietnamworks'),
        ('topcv', 'TopCV'),
    ]
    job_portal = models.CharField(max_length=50, blank=True, null=True, choices=SOURCE_CHOICES)
    job_title = models.CharField(max_length=511, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    searching_location = models.CharField(max_length=255, blank=True, null=True)


class JobTitleSearchTerm(models.Model):
    term = models.CharField(max_length=255, blank=True, null=True)


class LocationSearchTerm(models.Model):
    term = models.CharField(max_length=255, blank=True, null=True)
