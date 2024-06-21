# Generated by Django 3.2.22 on 2024-06-20 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corecode', '0034_alter_schedule_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]