# Generated by Django 5.0.6 on 2024-10-13 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='company',
            field=models.ManyToManyField(to='jobportal_app.company'),
        ),
    ]