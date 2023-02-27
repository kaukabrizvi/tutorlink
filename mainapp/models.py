class Profile(models.Model):
        REQUIRED_FIELDS = ('user',)
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
        is_tutor = models.BooleanField(verbose_name="is_tutor", default=False)
        is_student = models.BooleanField(verbose_name="is_student", default=False)
        def __str__(self):
                return str(self.user)

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, kwargs):
                if created:
                        Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, kwargs):
                instance.profile.save()
