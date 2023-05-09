from django.contrib import admin

from .models import JobPosting


# admin.site.register(Resume)
@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    # List View
    list_display = ["id", "job_portal", "job_title", "company", "date", "searching_location"]
    list_filter = ("job_portal", "searching_location")
