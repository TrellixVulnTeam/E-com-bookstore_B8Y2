from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from books.models import Book

User = settings.AUTH_USER_MODEL



class SaveManager(models.Manager):
    def new_or_get(self, request):    
        cart_id = request.session.get("cart_id", None) #get the current cart ID or say None
        qs = self.get_queryset().filter(id=cart_id) #ttttttt
        if qs.count() == 1: # check if the cart exist
            new_obj = False
            cart_obj = qs.first() # if the cart exist set the same object to 
            if '''request.user.is_authenticated()''' and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else: 
            cart_obj = self.new(user=request.user)  #create a new one 
            new_obj = True
            request.session['cart_id'] = cart_obj.id # and start a new section
        return cart_obj, new_obj #return the car and whether or not is new
    def new(self, user=None):
        user_obj = None
        if user is not None:
            #if user.is_authenticated():
            user_obj = user
        return self.model.objects.create(user=user_obj)

# create fields
class Save(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    products    = models.ManyToManyField(Book, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)    
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    objects = SaveManager()
    def __str__(self):
        return str(self.id) # id of the cart





