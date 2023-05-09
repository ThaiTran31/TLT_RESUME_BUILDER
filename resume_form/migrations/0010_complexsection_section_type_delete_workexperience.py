# Generated by Django 4.0.8 on 2023-02-07 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_form', '0009_alter_skill_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='complexsection',
            name='section_type',
            field=models.CharField(blank=True, choices=[('employment_histories', 'Employment History'), ('educations', 'Education'), ('skills', 'Skill'), ('links', 'Link'), ('customs', 'Custom')], default='customs', max_length=20),
        ),
        migrations.DeleteModel(
            name='WorkExperience',
        ),
    ]
