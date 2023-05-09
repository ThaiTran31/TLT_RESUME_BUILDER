import sys
from django.contrib import admin

from .models import Resume
from resume_form.admin import PersonalDetailsInline, ProfessionalSummaryInline, ComplexSectionInline
sys.path.append("..")


# admin.site.register(Resume)
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    # List View
    list_display = ["id", "title", "user", "template", "completeness", "created_at", "updated_at", ]
    list_filter = ("user",)
    # Detail View
    fields = ["title", "template", "layout", "completeness", "user", "image", "thumbnail"]
    inlines = [PersonalDetailsInline, ProfessionalSummaryInline, ComplexSectionInline]
