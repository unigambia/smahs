# Generated by Django 3.2.22 on 2024-06-18 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staffs', '0013_staff_created_at_staff_created_by_staff_updated_at_and_more'),
        ('corecode', '0026_courseregistrationperiod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.course')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_created_by', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staffs.staff')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('staff', 'course', 'day', 'start_time', 'end_time')},
            },
        ),
    ]
