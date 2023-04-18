# Generated by Django 4.1.1 on 2023-04-18 21:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0033_class_uuid_alter_class_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='id',
        ),
        migrations.AlterField(
            model_name='class',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
