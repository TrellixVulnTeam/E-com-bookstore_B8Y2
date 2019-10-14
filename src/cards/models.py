from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

CARD_TYPE = (
    ('visa', 'Visa'),
    ('mastercard', 'Mastercard'),
    ('amex', 'Amex'),
    ('discover', 'Discover'),
)

class Cards (models.Model):
    class Meta:
        verbose_name_plural = 'Cards'

    User = settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=120, choices = CARD_TYPE)
    name_on_card = models.CharField(max_length=120)
    card_number = models.CharField(max_length=120)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    ccv_code = models.CharField (max_length = 4)
   
    def __str__(self):
        return f'{self.user} Cards'


