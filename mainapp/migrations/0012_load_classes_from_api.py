# Generated by Django 4.1.5 on 2023-04-06 17:28
from django.db import migrations
from mainapp.models import Class

def load_classes(apps, schema_editor):
    Class.load_from_api()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_profile_accepted_list'),
    ]

    operations = [
    ]