import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import generic
from .models import Book,Author
from accounts.models import WishList, WishListNames
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from random import shuffle
from carts.models import Cart


class AllAuthorsView(generic.TemplateView):
    template_name = 'book_author.html'

    def get_context_data(self, **kwargs):
        context = super(AllAuthorsView, self).get_context_data(**kwargs)
        context['a'] = Author.objects.filter(full_name__startswith="A")
        context['b'] = Author.objects.filter(full_name__startswith="B")
        context['c'] = Author.objects.filter(full_name__startswith="C")
        context['d'] = Author.objects.filter(full_name__startswith="D")
        context['e'] = Author.objects.filter(full_name__startswith="E")
        context['f'] = Author.objects.filter(full_name__startswith="F")
        context['g'] = Author.objects.filter(full_name__startswith="G")
        context['h'] = Author.objects.filter(full_name__startswith="H")
        context['i'] = Author.objects.filter(full_name__startswith="I")
        context['j'] = Author.objects.filter(full_name__startswith="J")
        context['k'] = Author.objects.filter(full_name__startswith="K")
        context['l'] = Author.objects.filter(full_name__startswith="L")
        context['m'] = Author.objects.filter(full_name__startswith="M")
        context['n'] = Author.objects.filter(full_name__startswith="N")
        context['o'] = Author.objects.filter(full_name__startswith="O")
        context['p'] = Author.objects.filter(full_name__startswith="P")
        context['q'] = Author.objects.filter(full_name__startswith="Q")
        context['r'] = Author.objects.filter(full_name__startswith="R")
        context['s'] = Author.objects.filter(full_name__startswith="S")
        context['t'] = Author.objects.filter(full_name__startswith="T")
        context['u'] = Author.objects.filter(full_name__startswith="U")
        context['v'] = Author.objects.filter(full_name__startswith="V")
        context['w'] = Author.objects.filter(full_name__startswith="W")
        context['x'] = Author.objects.filter(full_name__startswith="X")
        context['y'] = Author.objects.filter(full_name__startswith="Y")
        context['z'] = Author.objects.filter(full_name__startswith="Z")
        return context


class BookListView(generic.ListView):
    template_name = 'book_list.html'
    model = Book

    def get_queryset(self):
        order = self.request.GET.get("sort")
        order2 = self.request.GET.get("order")
        queryset_list = Book.objects.all()

        query = self.request.GET.get("q")  # this gets the contents from the search bar 'q'
        if query:
            if query in 'Tech Valley Times Best Sellers':
                queryset_list = queryset_list.filter(tech_valley_best=1)
            elif query in 'Coming Soon':
                queryset_list = queryset_list.filter(publication_date__gt=datetime.date.today())
            elif 'Star' in query:
                if 'One' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(1, 1.9))
                elif 'Two' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(2, 2.9))
                elif 'Three' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(3, 3.9))
                elif 'Four' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(4, 4.5))
                elif 'Five' in query:
                    queryset_list = queryset_list.filter(avg_rating__range=(4.6, 5))

            else:
                queryset_list = queryset_list.filter(title__icontains=query).distinct() | \
                                queryset_list.filter(authors__full_name__icontains=query).distinct() | \
                                queryset_list.filter(genre__icontains=query).distinct()

        if order:
            order = order.strip()
            if query and order2 and queryset_list.filter(genre__icontains=query):
                queryset_list = queryset_list.order_by(order, order2)
            else:
                if order == 'sales_rank':
                    queryset_list = queryset_list.order_by(order).exclude(sales_rank=0)
                else:
                    queryset_list = queryset_list.order_by(order)
        else:
            if query and order2 and queryset_list.filter(genre__icontains=query):
                queryset_list = queryset_list.order_by("-tech_valley_best", order2)
            else:
                queryset_list = queryset_list.order_by("title")

        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        queryset_list = self.get_queryset()
        display_sort = self.request.GET.get("display")
        order = self.request.GET.get("sort")
        order2 = self.request.GET.get("order")
       
        
        context['total'] = self.get_queryset().count()
        query = self.request.GET.get("q")

        if query:
            context['q'] = query

        if order:
            context['sort'] = order
            if order == 'title':
                context['sorting'] = "Title - A to Z"
            elif order == '-title':
                context['sorting'] = "Title - Z to A"
            elif order == '-avg_rating':
                context['sorting'] = "Top Rated"
            elif order == 'publication_date':
                context['sorting'] = "Oldest"
            elif order == '-publication_date':
                context['sorting'] = "Newest"
            elif order == 'authors':
                context['sorting'] = "Author(s) A - Z"
            elif order == '-authors':
                context['sorting'] = "Author(s) Z - A"
            elif order == 'price':
                context['sorting'] = "Price - Low to High"
            elif order == '-price':
                context['sorting'] = "Price - High to Low"
            elif order == 'sales_rank':
                context['sorting'] = "Top Sellers"
            elif order == '-tech_valley_best':
                context['sorting'] = "Tech Valley Best Sellers"
        else:
            if query and Book.objects.filter(genre__icontains=query):
                context['sort'] = "-tech_valley_best"
                context['order'] = "-rating"
                context['sorting'] = "Tech Valley Best Sellers"
            else:
                context['sort'] = "title"
                context['sorting'] = "Title - A to Z"

        if display_sort:
            if queryset_list.count() > int(display_sort):
                context['display_sort_num'] = display_sort
            else:
                context['display_sort_num'] = display_sort
        else:
            if queryset_list.count() > 10:
                context['display_sort_num'] = 10
            else:
                context['display_sort_num'] = 10

        if order2:
            context['order'] = order2

        return context

    def get_paginate_by(self, queryset):
        display_sort = self.request.GET.get("display")
        if display_sort:
            if queryset.count() > int(display_sort):
                paginate_by = display_sort
            else:
                paginate_by = queryset.count()
        else:
            if queryset.count() > 10:
                paginate_by = 10
            else:
                paginate_by = queryset.count()

        return paginate_by


class BookDetailView(generic.DetailView):
    template_name = 'book_detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        number = cart_count(self.request)
        context['number'] = number
        author = Author.objects.filter(book=self.kwargs.get("pk")).distinct()
        context['author_books'] = Book.objects.filter(authors__book__authors__in=author).distinct().exclude(
        pk=self.kwargs.get("pk"))
        return context


def book_list_view(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    temp_list = []
    if request.method == 'POST':
        search_book = request.POST.get('book-field')
        search_result = []
        for item in books:
            if search_book.lower() in item.title.lower():
                search_result.append(item)
            else:
                for auth in item.authors.all():
                    if search_book.lower() in auth.full_name.lower():
                        search_result.append(item)
        if not search_result:
            messages.info(request, 'No match found..!')

        for item in search_result:
            temp_list.append(item.id)
        request.session['book_list'] = temp_list

        page = request.GET.get('page', 1)

        paginator = Paginator(search_result, 12)
        try:
            book_by_page = paginator.page(page)
        except PageNotAnInteger:
            book_by_page = paginator.page(1)
        except EmptyPage:
            book_by_page = paginator.page(paginator.num_pages)

        context = {'book_by_page': book_by_page}
        return render(request, 'book_list.html', context)

    for item in books:
        temp_list.append(item.id)
    request.session['book_list'] = temp_list

    page = request.GET.get('page', 1)

    paginator = Paginator(books, 12)
    try:
        book_by_page = paginator.page(page)
    except PageNotAnInteger:
        book_by_page = paginator.page(1)
    except EmptyPage:
        book_by_page = paginator.page(paginator.num_pages)

    context = {'book_by_page': book_by_page}
    return render(request, 'book_list.html', context)


def book_detail_view(request, index):
    wishlist_names = WishListNames.objects.all()
    wishlist_names_d = {}
    for w in wishlist_names:
        wishlist_names_d[w.wishlist_num] = w

    author = Author.objects.filter(book=index).distinct()
    book_authors = Book.objects.filter(authors__book__authors__in=author).distinct()
    for book in Book.objects.all():
        
        if str(book.id) == str(index):
            return render(request, 'book_detail.html', {'book': book, 'author':author, 'author_books':book_authors, 'wishlists': wishlist_names_d})


def refined_view(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        price_min = request.POST.get('price_min')
        price_max = request.POST.get('price_max')
        rating = request.POST.get('rating')
        search_result = []

        for item in books:
            if title:
                if title.lower() in item.title.lower():
                    title_flag = 1
                else:
                    title_flag = 0
            else:
                title_flag = 1

            if author:
                author_flag = 0
                for auth in item.authors.all():
                    if author.lower() in auth.full_name.lower():
                        author_flag = 1
            else:
                author_flag = 1

            if genre:
                if genre.lower() in item.genre.lower():
                    genre_flag = 1
                else:
                    genre_flag = 0
            else:
                genre_flag = 1

            if price_min and price_max:
                if float(price_min) <= item.price <= float(price_max):
                    price_flag = 1
                else:
                    price_flag = 0
            else:
                price_flag = 1

            if rating:
                if float(rating) <= item.avg_rating:
                    rating_flag = 1
                else:
                    rating_flag = 0
            else:
                rating_flag = 1

            if title_flag == 1 and author_flag == 1 and genre_flag == 1 and price_flag == 1 and rating_flag == 1:
                search_result.append(item)

        if not search_result:
            messages.info(request, 'No match found..!')
        else:
            temp_list = []
            for item in search_result:
                temp_list.append(item.id)
            request.session['book_list'] = temp_list


        page = request.GET.get('page', 1)

        paginator = Paginator(search_result, 12)
        try:
            book_by_page = paginator.page(page)
        except PageNotAnInteger:
            book_by_page = paginator.page(1)
        except EmptyPage:
            book_by_page = paginator.page(paginator.num_pages)

        context = {'book_by_page': book_by_page}
        return render(request, 'book_list.html', context)

    page = request.GET.get('page', 1)

    paginator = Paginator(books, 12)
    try:
        book_by_page = paginator.page(page)
    except PageNotAnInteger:
        book_by_page = paginator.page(1)
    except EmptyPage:
        book_by_page = paginator.page(paginator.num_pages)

    context = {'book_by_page': book_by_page}
    return render(request, 'book_list.html', context)


def sorted_book(request):
    if request.method == 'POST':
        value = request.POST.get('sort_values')
        book_list = []
        list = request.session['book_list']
        for x in list:
            for item in Book.objects.all():
                if item.id == x:
                    book_list.append(item)
        if value == 'low':
            book_list.sort(key=lambda x: x.price, reverse=False)
        elif value == 'high':
            book_list.sort(key=lambda x: x.price, reverse=True)
        else:
            shuffle(book_list)
        page = request.GET.get('page', 1)

        paginator = Paginator(book_list, 12)
        try:
            book_by_page = paginator.page(page)
        except PageNotAnInteger:
            book_by_page = paginator.page(1)
        except EmptyPage:
            book_by_page = paginator.page(paginator.num_pages)

        context = {'book_by_page': book_by_page,'value':value}
        return render(request, 'book_list.html', context)
