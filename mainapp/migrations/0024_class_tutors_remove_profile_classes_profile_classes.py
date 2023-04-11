# Generated by Django 4.1.5 on 2023-04-11 15:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0023_alter_profile_schedule_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='tutors',
            field=models.ManyToManyField(blank=True, related_name='tutors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='classes',
        ),
        migrations.AddField(
            model_name='profile',
            name='classes',
            field=models.ManyToManyField(blank=True, related_name='classes', to='mainapp.class'),
        ),
    ]