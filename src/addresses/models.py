from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping','Shipping'),
)


class AddressManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        created = False
        obj = None
        if user.is_authenticated():
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        else:
            pass
        return obj, created
        
class Address(models.Model):
    class Meta:
        verbose_name_plural = 'Addresses'
    User = settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    address_type = models.CharField(max_length=120, choices= ADDRESS_TYPE)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length= 120, null =True, blank = True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default = 'United States of America')

    objects = AddressManager()
    
    def __str__(self):
        return f'{self.user} Address'

    


