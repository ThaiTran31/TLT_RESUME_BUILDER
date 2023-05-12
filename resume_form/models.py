from email.policy import default
from django.db import models

from resume.models import Resume


class PersonalDetails(models.Model):
    header = models.CharField(max_length=100, default="Personal Details")
    resume = models.OneToOneField(Resume, related_name="personal_details", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    job_title = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    nationality = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    place_of_birth = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)


class ProfessionalSummary(models.Model):
    header = models.CharField(max_length=100, default="Professional Summary")
    resume = models.OneToOneField(Resume, related_name="professional_summary", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=2)
    content = models.TextField(null=True, blank=True)


class ComplexSection(models.Model):
    header = models.CharField(max_length=100, default="Untitled")
    resume = models.ForeignKey(Resume, related_name="complex_sections", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    SECTION_TYPE = (
        ("employment_histories", "Employment History"),
        ("educations", "Education"),
        ("skills", "Skill"),
        ("links", "Link"),
        ("customs", "Custom"),
    )
    section_type = models.CharField(
        max_length=20,
        choices=SECTION_TYPE,
        blank=True,
        default="customs",
    )

    def __str__(self):
        return f'{self.resume} - {self.section_type}'


class EmploymentHistory(models.Model):
    complex_section = models.ForeignKey(ComplexSection, related_name="employment_histories", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    job_title = models.TextField(null=True, blank=True)
    employer = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.complex_section} - item {self.position}'


class Education(models.Model):
    complex_section = models.ForeignKey(ComplexSection, related_name="educations", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    school = models.TextField(null=True, blank=True)
    degree = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.complex_section} - item {self.position}'


class Custom(models.Model):
    complex_section = models.ForeignKey(ComplexSection, related_name="customs", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    title = models.TextField(help_text="Activity name, Job title, Book title etc.", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.complex_section} - item {self.position}'


class Skill(models.Model):
    complex_section = models.ForeignKey(ComplexSection, related_name="skills", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    SKILL_LEVEL = (
        ("novice", "Novice"),
        ("beginner", "Beginner"),
        ("skillful", "Skillful"),
        ("experienced", "Experienced"),
        ("expert", "Expert"),
    )
    name = models.TextField(null=True, blank=True)
    level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL,
        blank=True,
        default="beginner",
    )

    def __str__(self):
        return f'{self.complex_section} - item {self.position}'


class Link(models.Model):
    complex_section = models.ForeignKey(ComplexSection, related_name="links", on_delete=models.CASCADE, null=True)
    position = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    label = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.complex_section} - item {self.position}'
