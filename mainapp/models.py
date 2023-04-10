from django.db import models, transaction
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests

class TutorSesh(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "tutor_scheduled")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "student_scheduled")
    date = models.DateField()
    time = models.TimeField()

class Profile(models.Model):
        REQUIRED_FIELDS = ('user',)
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
        is_tutor = models.BooleanField(verbose_name="is_tutor", default=False)
        is_student = models.BooleanField(verbose_name="is_student", default=False)
        classes = models.JSONField(default=[])
        connected_list = models.ManyToManyField(User,related_name="connected_list", blank=True)
        accepted_list = models.ManyToManyField(User,related_name="accepted_list", blank=True)
        schedule_list = models.ManyToManyField(TutorSesh, related_name="schedule_list", blank=True)
        def __str__(self):
                return str(self.user)

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
                if created:
                        Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
                instance.profile.save()

class Class(models.Model):
    subject = models.CharField(max_length=50)
    catalog_nbr = models.CharField(max_length=50)
    descr = models.TextField()


    def __str__(self):
        return f"{self.subject} {self.catalog_nbr} - {self.descr}"
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
