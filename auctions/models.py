from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=64)
    address = models.CharField(max_length=255, blank=True, null=True,
                               verbose_name='Delivery address (optional)')


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    min_price = models.DecimalField(max_digits=7, decimal_places=2,
                                    verbose_name='Min. price [$]',
                                    validators=[MinValueValidator(1)])
    current_price = models.DecimalField(max_digits=7, decimal_places=2,
                                        verbose_name='Current price [$]',
                                        null=True)
    category = models.ManyToManyField(Category, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def get_current_price(self):
        """
        Checks if the Auction instance has any bids and returns the highest,
        otherwise assigns self.min_price as self.current_price.
        :return: self.current_price
        """
        highest_bid = Bid.objects.filter(auction=self).aggregate(
            models.Max('price')
        )
        if highest_bid:
            self.current_price = highest_bid['price__max']
        else:
            self.current_price = self.min_price
        return self.current_price

    def save(self, *args, **kwargs):
        if not self.current_price:
            self.current_price = self.min_price
        super().save(*args, **kwargs)


class Bid(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                verbose_name='')


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='')


class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
