# shopping cart version 
from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from books.models import Book
from django.db.models.signals import pre_save, post_save, m2m_changed

 

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):    
        cart_id = request.session.get("cart_id", None) #get the current cart ID or say None
        qs = self.get_queryset().filter(id=cart_id) #ttttttt
        if qs.count() == 1: # check if the cart exist
            new_obj = False
            cart_obj = qs.first() # if the cart exist set the same object to tttttttt
            if '''request.user.is_authenticated()''' and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else: 
            cart_obj = Cart.objects.new(user=request.user)  #create a new one 
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
class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # triy models.OneToMany(same)
    products    = models.ManyToManyField(Book, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)    
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    objects = CartManager()
    def __str__(self):
        return str(self.id) # id of the cart


# calculate the subtotal
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0 
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


# calculate total
def pre_save_cart_receiver(sender, instance, *arg, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10 # adding taxes
    else:
        instance.total = 0.00
pre_save.connect(pre_save_cart_receiver, sender=Cart)


