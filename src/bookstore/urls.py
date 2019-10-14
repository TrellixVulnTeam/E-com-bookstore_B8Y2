from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('about/', views.about, name='home_about'),
    path('wishlist/', views.wishlist_default, name='wish_list_default'),
    path('wishlist/<int:wishlistID>', views.wishlist, name='wish_list'),
    path('create-wishlist/<int:userID>/<int:wishlistID>/<str:name>', views.create_wistlist, name='create_wishlist'),
    path('delete-wishlist/<int:userID>/<int:wishlistID>', views.delete_wistlist, name='create_wishlist'),
    path('edit-wishlist/<int:wishlistID>/<str:name>', views.edit_wistlist, name='edit_wishlist'),
    path('add-to-wishlist/<int:wishlistID>/<int:bookID>', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlistID>/<int:bookID>', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move-to-wishlist/<int:bookId>/<int:wishlistID1>/<int:wishlistID2>', views.move_wistlist, name='move_to_wishlist')
]