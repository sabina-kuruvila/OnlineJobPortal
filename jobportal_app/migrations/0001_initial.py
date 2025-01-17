# Generated by Django 5.1.2 on 2024-10-09 17:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('salary', models.IntegerField(null=True)),
                ('experience', models.IntegerField()),
                ('location', models.CharField(max_length=2000, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('DOB', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('Male', 'male'), ('Female', 'female'), ('Other', 'other')], max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(max_length=2000)),
                ('resume', models.FileField(null=True, upload_to='resumes/')),
                ('company', models.ManyToManyField(blank=True, to='jobportal_app.company')),
            ],
        ),
    ]
