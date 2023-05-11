from django.db import models


class ResumeTemplate(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='resume_template_thumbnails/', null=True, blank=True)
    CATEGORY_CHOICES = [
        ('creative', 'Creative'),
        ('simple', 'Simple'),
        ('professional', 'Professional'),
        ('modern', 'Modern')
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='creative')

    def __str__(self):
        return self.title
