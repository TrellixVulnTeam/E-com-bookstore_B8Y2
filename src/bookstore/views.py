from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from books.models import Book,Author
from accounts.models import WishList, WishListNames
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


def home(request):
    books = Book.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(books, 12)
    try:
        book_by_page = paginator.page(page)
    except PageNotAnInteger:
        book_by_page = paginator.page(1)
    except EmptyPage:
        book_by_page = paginator.page(paginator.num_pages)

    context = {'book_by_page': book_by_page}
    return render(request, 'bookstore/home.html', context)
# Create your views here.

def about(request):
    return render(request, 'bookstore/about.html')

def create_wistlist(request, userID, wishlistID, name):
    user = User.objects.get(id=userID)
    WishListNames(user=user, wishlist_num=wishlistID, name=name).save()
    return JsonResponse({'msg':'Success'})

def edit_wistlist(request, wishlistID, name):
    wishlistItem = WishListNames.objects.filter(user=request.user, wishlist_num=wishlistID)
    wishlistItem.update(name=name)
    return JsonResponse({'msg':'Success'})

def delete_wistlist(request, userID, wishlistID):
    user = User.objects.get(id=userID)
    WishList.objects.filter(wishlist_num=wishlistID).delete()
    WishListNames.objects.get(user=user, wishlist_num=wishlistID).delete()
    return JsonResponse({'msg':'Success'})

def add_to_wishlist(request, wishlistID, bookID):
    if WishList.objects.filter(user=request.user, book=Book.objects.get(id=bookID), wishlist_num=wishlistID).exists():
        return JsonResponse({'msg':'Already exists'})
    wishlistItem = WishList(user=request.user, book=Book.objects.get(id=bookID), wishlist_num=wishlistID)
    wishlistItem.save()
    return JsonResponse({'msg':'Success'})

def move_wistlist(request, bookId, wishlistID1, wishlistID2):
    wishlistitem = WishList.objects.filter(user=request.user, book=Book.objects.get(id=bookId), wishlist_num=wishlistID1)
    wishlistitem2 = WishList.objects.filter(user=request.user, book=Book.objects.get(id=bookId), wishlist_num=wishlistID2)
    if not wishlistitem2:
        WishList(user=request.user, book=Book.objects.get(id=bookId), wishlist_num=wishlistID2).save()
    if wishlistitem:
        wishlistitem.delete()
    return JsonResponse({'msg':'Success'})

def remove_from_wishlist(request, wishlistID, bookID):
    wishlistItem = WishList.objects.filter(user=request.user, book=Book.objects.get(id=bookID), wishlist_num=wishlistID)
    if wishlistItem:
        wishlistItem.delete()
    return JsonResponse({'msg':'Success'})

def wishlist_default(request):
    return redirect('/wishlist/0')

def wishlist(request, wishlistID):
    wishlist_names = WishListNames.objects.all()
    wishlist = WishList.objects.filter(user=request.user)
    wishlist_names_d = [None, None, None]
    for w in wishlist_names:
        wishlist_names_d[w.wishlist_num] = w

    context = {
        "wishlist": wishlist,
        "wishlistNames": wishlist_names_d,
        "numWishlist": range(3),
        "wishlistNum": wishlistID
    }

    return render(request, 'bookstore/wishlist.html', context)
