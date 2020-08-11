from django.conf import Settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# User = Settings.AUTH_USER_MODEL
User = User


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


def post_save_user_created_receiver(sender, instance, created, *args, **kwargs):
    """
     this post save receiver adds
     registered user's email to BillingProfile
    """
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(post_save_user_created_receiver, sender=User)