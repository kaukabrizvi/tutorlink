# Generated by Django 4.1.7 on 2023-04-30 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_profile_rating_profile_review_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
