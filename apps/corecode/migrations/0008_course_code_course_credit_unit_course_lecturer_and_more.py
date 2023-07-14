# Generated by Django 4.2.2 on 2023-07-03 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("staffs", "0007_staff_image"),
        ("corecode", "0007_rename_studentclass_studentcohort_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="code",
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="course",
            name="credit_unit",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="course",
            name="lecturer",
            field=models.ForeignKey(
                limit_choices_to={"role": "academic"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="staffs.staff",
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="level",
            field=models.IntegerField(default=0),
        ),
    ]
