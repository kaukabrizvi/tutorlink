# Generated by Django 3.2.18 on 2023-05-02 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20230502_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='wednesday',
            field=models.BooleanField(default=False),
        ),
    ]