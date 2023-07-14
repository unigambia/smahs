# Generated by Django 4.2.2 on 2023-07-03 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffs", "0002_auto_20201124_0614"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="role",
            field=models.CharField(
                choices=[("admin", "Admin"), ("academic", "Academic")],
                default="academic",
                max_length=10,
            ),
        ),
    ]
