# Generated by Django 4.1.7 on 2023-04-05 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_alter_profile_schedule_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='schedule_list',
        ),
    ]
