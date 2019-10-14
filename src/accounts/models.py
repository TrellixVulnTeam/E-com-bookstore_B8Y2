from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from books.models import Book

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class WishListNames(models.Model):
    class Meta:
        unique_together = (('user', 'wishlist_num'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist_num = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(0), MinValueValidator(2)]
    )
    name = models.CharField(max_length=120)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    wishlist_num = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(0), MinValueValidator(2)]
    )

    def __str__(self):
        return f'{self.user.username}, {self.book.title}'


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
