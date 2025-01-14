# Generated by Django 5.1.2 on 2024-10-20 11:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal_app', '0004_alter_company_description_alter_company_experience_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='description',
        ),
        migrations.RemoveField(
            model_name='company',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='company',
            name='position',
        ),
        migrations.RemoveField(
            model_name='company',
            name='salary',
        ),
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='HR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal_app.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(max_length=2000, null=True)),
                ('experience', models.IntegerField(null=True)),
                ('salary', models.IntegerField(null=True)),
                ('location', models.CharField(max_length=2000, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jobportal_app.company')),
            ],
        ),
    ]
