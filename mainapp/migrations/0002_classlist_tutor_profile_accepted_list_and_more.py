# Generated by Django 4.1.1 on 2023-04-18 22:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.JSONField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='accepted_list',
            field=models.ManyToManyField(blank=True, related_name='accepted_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='avail_end',
            field=models.TimeField(default=datetime.time(23, 59, 59)),
        ),
        migrations.AddField(
            model_name='profile',
            name='avail_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='connected_list',
            field=models.ManyToManyField(blank=True, related_name='connected_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_student',
            field=models.BooleanField(default=False, verbose_name='is_student'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_tutor',
            field=models.BooleanField(default=False, verbose_name='is_tutor'),
        ),
        migrations.AddField(
            model_name='profile',
            name='monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='000-000-0000', max_length=12),
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
        migrations.CreateModel(
            name='TutorSesh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_scheduled', to=settings.AUTH_USER_MODEL)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_scheduled', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.tutor')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=50)),
                ('catalog_nbr', models.CharField(max_length=50)),
                ('descr', models.TextField()),
                ('tutors', models.ManyToManyField(blank=True, default=[], related_name='tutors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='classes',
            field=models.ManyToManyField(blank=True, related_name='classes', to='mainapp.class'),
        ),
        migrations.AddField(
            model_name='profile',
            name='schedule_list',
            field=models.ManyToManyField(blank=True, related_name='schedule_list', to='mainapp.tutorsesh'),
        ),
    ]
