from django.contrib import admin

from .models import JobPosting, JobTitleSearchTerm, LocationSearchTerm


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    # List View
    list_display = ["id", "job_portal", "job_title", "company", "date", "searching_location"]
    list_filter = ("job_portal", "searching_location")


@admin.register(JobTitleSearchTerm)
class JobTitleSearchTermAdmin(admin.ModelAdmin):
    # List View
    list_display = ["id", "term"]


@admin.register(LocationSearchTerm)
class LocationSearchTermAdmin(admin.ModelAdmin):
    # List View
    list_display = ["id", "term"]
