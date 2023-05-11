from django.contrib import admin

from .models import PersonalDetails, ProfessionalSummary, ComplexSection, EmploymentHistory, Education, Custom, Skill, Link


# admin.site.register(PersonalDetails)
# admin.site.register(ProfessionalSummary)
# admin.site.register(ComplexSection)
# admin.site.register(EmploymentHistory)
# admin.site.register(Education)
# admin.site.register(Custom)
# admin.site.register(Skill)
# admin.site.register(Link)
@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "resume", "header"]


class PersonalDetailsInline(admin.TabularInline):
    extra = 0
    model = PersonalDetails


@admin.register(ProfessionalSummary)
class ProfessionalSummaryAdmin(admin.ModelAdmin):
    list_display = ["id", "resume", "header"]


class ProfessionalSummaryInline(admin.TabularInline):
    extra = 0
    model = ProfessionalSummary


@admin.register(EmploymentHistory)
class EmploymentHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "complex_section", "position"]


class EmploymentHistoryInline(admin.TabularInline):
    extra = 0
    model = EmploymentHistory


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["id", "complex_section", "position"]


class EducationInline(admin.TabularInline):
    extra = 0
    model = Education


@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ["id", "complex_section", "position"]


class CustomInline(admin.TabularInline):
    extra = 0
    model = Custom


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["id", "complex_section", "position"]


class SkillInline(admin.TabularInline):
    extra = 0
    model = Skill


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["id", "complex_section", "position"]


class LinkInline(admin.TabularInline):
    extra = 0
    model = Link


@admin.register(ComplexSection)
class ComplexSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "resume", "header"]
    list_filter = ("resume",)
    inlines = [
        EmploymentHistoryInline, EducationInline,
        CustomInline, SkillInline, LinkInline,
    ]


class ComplexSectionInline(admin.TabularInline):
    extra = 0
    model = ComplexSection
