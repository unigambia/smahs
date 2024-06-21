# Generated by Django 3.2.22 on 2024-06-20 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0031_auto_20240619_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corecode.academicsemester'),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corecode.academicsession'),
        ),
    ]