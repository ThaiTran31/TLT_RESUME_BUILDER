# Generated by Django 4.0.8 on 2023-05-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_template', '0004_alter_resumetemplate_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumetemplate',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='resume_template_thumbnails/'),
        ),
    ]