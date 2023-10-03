# Generated by Django 4.2.2 on 2023-08-12 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("staffs", "0011_remove_staff_role"),
        ("corecode", "0011_studentcourse_registration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="lecturer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="lecturer",
                to="staffs.staff",
            ),
        ),
    ]