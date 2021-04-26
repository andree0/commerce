from django.contrib import admin
from .models import Auction, Bid, Category, Comment, User, Watchlist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    pass


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    pass
