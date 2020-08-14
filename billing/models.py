from django.conf import Settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from accounts.models import GuestEmail
User = User


class BillingManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        obj = None
        created = False
        if user.is_authenticated:
            """
            logged in user checkout, 
            will remember payment stuffs
            """
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)

        elif guest_email_id is not None:
            """
            Guest user checkout
            auto reloads payment stuffs
            """
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass

        return obj, created



class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    objects = BillingManager()


def post_save_user_created_receiver(sender, instance, created, *args, **kwargs):
    """
     this post save receiver adds
     registered user's email to BillingProfile
    """
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(post_save_user_created_receiver, sender=User)