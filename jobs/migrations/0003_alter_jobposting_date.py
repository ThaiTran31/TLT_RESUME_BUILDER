# Generated by Django 4.0.8 on 2023-05-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobposting_searching_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
