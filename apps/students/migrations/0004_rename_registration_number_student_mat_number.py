# Generated by Django 4.2.2 on 2023-07-13 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0003_rename_current_class_student_current_cohort"),
    ]

    operations = [
        migrations.RenameField(
            model_name="student",
            old_name="registration_number",
            new_name="mat_number",
        ),
    ]
