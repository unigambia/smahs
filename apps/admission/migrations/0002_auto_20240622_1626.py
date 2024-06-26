# Generated by Django 3.2.22 on 2024-06-22 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionapplication',
            name='Created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admissionapplication',
            name='Created_by',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='admissionapplication',
            name='Updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='admissionapplication',
            name='Updated_by',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='admissioncycle',
            name='Created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admissioncycle',
            name='Created_by',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='admissioncycle',
            name='Updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='admissioncycle',
            name='Updated_by',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
