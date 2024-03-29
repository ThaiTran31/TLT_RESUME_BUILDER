# Generated by Django 4.0.8 on 2022-10-14 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
        ('resume_form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplexSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='Untitled', max_length=100)),
                ('resume', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume.resume')),
            ],
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='resume',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume.resume'),
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, help_text="the project's name", null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('complex_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_form.complexsection')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('level', models.CharField(blank=True, choices=[('n', 'Novice'), ('b', 'Beginer'), ('s', 'Skillful'), ('e', 'Experienced'), ('m', 'Master')], default='b', max_length=1)),
                ('complex_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_form.complexsection')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='Professional Summary', max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('resume', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('complex_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_form.complexsection')),
            ],
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.TextField(blank=True, null=True)),
                ('employer', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('complex_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_form.complexsection')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.TextField(blank=True, null=True)),
                ('degree', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('complex_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_form.complexsection')),
            ],
        ),
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, help_text='Activity name, Job title, Book title etc.', null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('complex_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_form.complexsection')),
            ],
        ),
    ]
