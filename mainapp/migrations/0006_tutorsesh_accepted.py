# Generated by Django 4.1.7 on 2023-05-01 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_profile_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorsesh',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]