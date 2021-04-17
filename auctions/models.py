from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address (optional)')


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
                                    validators=[MinValueValidator(1)])
    current_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Current price [$]',
                                        null=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_current_price(self):
        highest_bid = Bid.objects.filter(auction=self).aggregate(models.Max('price'))
        if highest_bid:
            self.current_price = highest_bid['price__max']
            return self.current_price
        else:
            return null

    def save(self, *args, **kwargs):
        if self.current_price is None:
            self.current_price = self.get_current_price
        super().save(*args, **kwargs)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Your bid [$]')

    def save(self, *args, **kwargs):
        self.auction.save()
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    description = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
