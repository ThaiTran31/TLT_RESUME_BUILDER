# Generated by Django 4.0.8 on 2022-12-14 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_template', '0003_alter_resumetemplate_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumetemplate',
            name='category',
            field=models.CharField(choices=[('creative', 'Creative'), ('simple', 'Simple'), ('professional', 'Professional'), ('modern', 'Modern')], default='creative', max_length=50),
        ),
    ]
