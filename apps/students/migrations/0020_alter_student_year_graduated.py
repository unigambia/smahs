# Generated by Django 3.2.22 on 2024-06-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_student_year_graduated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year_graduated',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
