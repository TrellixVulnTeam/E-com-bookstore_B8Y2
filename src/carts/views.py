from django.shortcuts import render, redirect

from books.models import Book
from .models import Cart


# create or get a cart
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)    
    return render(request, "carts/home.html", {"cart": cart_obj})
    

# Function to update the cart .. add, remove
def cart_update(request):
    print(request)    
    product_id =  request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Book.objects.get(id=product_id) 
        except Book.DoesNotExist:
            print("show message to user, profuct is gone")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")    

# def check_out(request):
#     cart_obje, new_obj = Cart.objects.new_or_get(request)
#     return render(request, "carts/checkout.html", {})