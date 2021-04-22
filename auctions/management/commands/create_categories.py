from django.core.management.base import BaseCommand

from auctions.models import Category

CATEGORIES = [
    'AGD&RTV',
    'art',
    'automotive',
    'books',
    'children',
    'DIY',
    'electronics',
    'fashion',
    'games',
    'garden',
    'home',
    'music',
    'toys',
    'other'
]


class Command(BaseCommand):
    help = 'Create categories'

    def handle(self, *args, **options):
        for cat in CATEGORIES:
            if not Category.objects.filter(name=cat):
                Category.objects.create(
                    name=cat
                )
