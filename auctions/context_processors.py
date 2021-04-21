from .models import Category


def metadata(request):
    return {
        'categories': Category.objects.all(),
        'author': 'Andrzej Jończy',
        'ip_address': request.META['REMOTE_ADDR']
    }
