from django.shortcuts import render, redirect

from books.models import Book
from .models import Save



def cart_home(request):
    cart_obj, new_obj = Save.objects.new_or_get(request)
    # products = cart_obj.products.all()
    # total = 0 
    # for x in products:
    #     total += x.price
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, "saves/home.html", {"save": cart_obj})
    #cart":cart_obj

def cart_update(request):
    print(request.POST)    
    save_id =  request.POST.get('save_id')
    if save_id is not None:
        try:
            product_obj = Book.objects.get(id=save_id) 
        except Book.DoesNotExist:
            print("show message to user, profuct is gone")
            return redirect("save:home")
        cart_obj, new_obj = Save.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_save'] = cart_obj.products.count()
    return redirect("save:home")    