from django.db import models


class ResumeTemplate(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True)
    CATEGORY_CHOICES = [
        ('creative', 'Creative'),
        ('simple', 'Simple'),
        ('professional', 'Professional'),
        ('modern', 'Modern')
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='creative')

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        return 'http://127.0.0.1:8000' + '/media/images/' + self.title.lower() + '.png'
