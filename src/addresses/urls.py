from django.urls import path

from . import views

urlpatterns = [

    # path('', views.BookListView.as_view(), name="book_list"),
    # path('^(?P<pk>\d+)/$', views.BookDetailView.as_view(), name="book_detail"),
    path('', views.addressregister, name= 'address-home')
    


]
