# Generated by Django 4.2.2 on 2023-06-20 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_alter_invoice_options_and_more"),
        ("result", "0003_rename_term_result_semester"),
        ("corecode", "0005_rename_subject_course"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="AcademicTerm",
            new_name="AcademicSemester",
        ),
    ]
