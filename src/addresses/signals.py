from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Address


@receiver(post_save, sender=Address)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(addresses=instance)


@receiver(post_save, sender=Address)
def save_address(sender, instance,  **kwargs):
    instance.addresses.save()
