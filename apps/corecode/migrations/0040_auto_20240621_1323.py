# Generated by Django 3.2.22 on 2024-06-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0039_auto_20240621_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminalert',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='admin_alerts'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='announcements'),
        ),
    ]
