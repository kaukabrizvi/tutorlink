from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests

class Profile(models.Model):
        REQUIRED_FIELDS = ('user',)
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
        is_tutor = models.BooleanField(verbose_name="is_tutor", default=False)
        is_student = models.BooleanField(verbose_name="is_student", default=False)
        classes = models.JSONField(default=[])
        def __str__(self):
                return str(self.user)

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
                if created:
                        Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
                instance.profile.save()

class Course(models.Model):
    subject = models.CharField(max_length=100)
    catalog_number = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.CharField(max_length=255)
    credits = models.IntegerField()
    prereqs = models.TextField(blank=True)
    coreqs = models.TextField(blank=True)
    term = models.CharField(max_length=6)
    meeting_times = models.JSONField(default=list)

    def __str__(self):
        return f"{self.subject} {self.catalog_number} - {self.title}"
class ClassList(models.Model):
    API_URL = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=CS&page=1"

    classes = models.JSONField(default=[])

    @classmethod
    def load_classes(cls):
        response = requests.get(cls.API_URL)
        if response.status_code == 200:
            cls.objects.update_or_create(id=1, defaults={"classes": response.json()})
        else:
            raise Exception(f"Failed to load classes: {response.status_code}")

    @classmethod
    def get_classes(cls):
        if not cls.objects.filter(id=1).exists():
            cls.load_classes()
        return cls.objects.get(id=1).classes