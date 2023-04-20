from django.db import models, transaction
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests
import datetime
import uuid


class TutorSesh(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "tutor_scheduled")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "student_scheduled")
    date = models.DateField()
    time = models.TimeField()
class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=50)
    catalog_nbr = models.CharField(max_length=50)
    descr = models.TextField()
    tutors = models.ManyToManyField(User, related_name="tutors", blank=True, default=[])
    title = str(subject) + " " + str(catalog_nbr)
    def __str__(self):
        return f"{self.subject} {self.catalog_nbr} - {self.descr}"

class Profile(models.Model):
        REQUIRED_FIELDS = ('user',)
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
        is_tutor = models.BooleanField(verbose_name="is_tutor", default=False)
        is_student = models.BooleanField(verbose_name="is_student", default=False)
        classes = models.ManyToManyField(Class, related_name="classes", blank=True)
        connected_list = models.ManyToManyField(User,related_name="connected_list", blank=True)
        accepted_list = models.ManyToManyField(User,related_name="accepted_list", blank=True)
        schedule_list = models.ManyToManyField(TutorSesh, related_name="schedule_list", blank=True)

        phone_number = models.CharField(max_length=12, default="000-000-0000")
        monday = models.BooleanField(default=False)
        tuesday = models.BooleanField(default=False)
        wednesday = models.BooleanField(default=False)
        thursday = models.BooleanField(default=False)
        friday = models.BooleanField(default=False)
        saturday = models.BooleanField(default=False)
        sunday = models.BooleanField(default=False)
        hourly_rate = models.DecimalField(default=10,decimal_places=2,max_digits=5)

        avail_start = models.TimeField(default=datetime.time(0,0,0))
        avail_end = models.TimeField(default=datetime.time(23,59,59))

        def __str__(self):
                return str(self.user)

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
                if created:
                        Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
                instance.profile.save()



class Review(models.Model):
    tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
class Tutor(models.Model):
    name = models.CharField(max_length=255)

    def update_rating(self):
        reviews = self.review_set.all()
        if reviews:
            self.rating = sum([r.rating for r in reviews]) / len(reviews)
            self.save()
        else:
            self.rating = 0
            self.save()
    name = models.CharField(max_length=255)
