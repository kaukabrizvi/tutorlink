class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")


        def str(self):
                return str(self.user)

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, kwargs):
                if created:
                        Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, kwargs):
                instance.profile.save()
