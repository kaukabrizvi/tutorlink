# Generated by Django 4.1.7 on 2023-04-16 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0029_tutor_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='hourly_rate',
            field=models.IntegerField(default=10),
        ),
    ]