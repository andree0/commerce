from .models import Auction, Category, Watchlist


def metadata(request):
    return {
        'categories': Category.objects.all(),
        'watchlist_count': Watchlist.objects.filter(user=request.user).count() if
        request.user.is_authenticated else None,
        'your_auction_count': Auction.objects.filter(owner=request.user).count() if
        request.user.is_authenticated else None,
        'author': 'Andrzej Jończy',
        'ip_address': request.META['REMOTE_ADDR']
    }
