# Generated by Django 4.1.5 on 2023-05-02 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_profile_cellphone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cellphone',
        ),
    ]