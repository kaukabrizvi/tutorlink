# Generated by Django 3.2.18 on 2023-05-02 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avail_end',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='avail_start',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='friday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='saturday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sunday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='wednesday',
        ),
        migrations.AddField(
            model_name='profile',
            name='fri_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='fri_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='mon_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='mon_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='sat_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='sat_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='sun_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='sun_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='thu_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='thu_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='tue_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='tue_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='wed_avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='wed_avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]
