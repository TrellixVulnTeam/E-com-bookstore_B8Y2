from django.conf import settings 
from django.db import models
from django.db.models.signals import post_save
from accounts.models import GuestEmail

# Create your models here.

User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user    = request.user
        guest_email_id = request.session.get('guest_email_id')
        create = False
        obj = None
        if user.is_authenticated():
            obj, create = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, created



class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("Send to stripe/braintree")
        instance.customer_id = newID
        instance.save()


def user_created_receiver(sender, instance , created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email = instance.email)

post_save.connect(user_created_receiver, sender=User)
