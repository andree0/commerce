from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    min_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Min. price [$]',
                                    validators=[MinValueValidator(0)])
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Your bid [$]')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    description = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)