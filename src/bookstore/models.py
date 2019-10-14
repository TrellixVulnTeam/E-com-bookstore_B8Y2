from django.db import models
from django.db.models import Avg
from django.utils.timezone import now


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    dob = models.CharField(max_length=12, null=True, blank=True)
    birthplace = models.CharField(max_length=75, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return u'%s' % self.full_name

    def get_absolute_url(self):
        return "/book/author/%s/" % self.id

    class Meta:
        ordering = ['full_name']

class Book(models.Model):
    authors = models.ManyToManyField(Author, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=600, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    publication_date = models.CharField(max_length=12, null=True, blank=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    pages = models.IntegerField(default=0)
    avg_rating = models.DecimalField(decimal_places=1, max_digits=2, default=0)
    sales_rank = models.IntegerField(default=0)
    top_sellers = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # def __str__(self):
    #     return self.title

    def get_absolute_url(self):
        return "/book/%s/" % self.id

    # def author(self):
    #     return Author.objects.filter(book__authors__book=self.id).distinct()

    def rating_avg(self):
        book = Book.objects.get(id=self.id)
        # return list(book.rating_set.aggregate(Avg('rating')).values())[0]
        pass

    def rating_count(self):
        # return Rating.objects.all().filter(book=self).count()
        pass

    class Meta:
        ordering = ['title']