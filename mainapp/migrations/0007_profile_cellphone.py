# Generated by Django 4.1.5 on 2023-05-01 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_tutorsesh_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cellphone',
            field=models.BooleanField(default=False),
        ),
    ]
