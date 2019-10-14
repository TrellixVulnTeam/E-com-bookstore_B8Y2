from django.urls import path

from . import views

urlpatterns = [

    # path('', views.BookListView.as_view(), name="book_list"),
    # path('^(?P<pk>\d+)/$', views.BookDetailView.as_view(), name="book_detail"),
    path('', views.book_list_view, name="book_list"),
    path('details/<int:index>/',views.book_detail_view, name='book_detail'),
    path('refined-search/', views.refined_view, name="refined_view"),
    path('sorted/', views.sorted_book, name="sorted"),
    path('books/', views.book_list_view)
    

]

