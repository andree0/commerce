from django.contrib import admin

from auctions.models import (
    Auction,
    Bid,
    Category,
    Comment,
    CustomUser,
    Watchlist,
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email', 'address', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'min_price', 'category', 'image', )


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    pass
