from django.core.management.base import BaseCommand

from auctions.models import Category


CATEGORIES = [
    "AGD&RTV",
    "antiques",
    "art",
    "automotive",
    "beauty",
    "books",
    "children",
    "culture",
    "DIY",
    "electronics",
    "entertainment",
    "fashion",
    "furniture",
    "games",
    "garden",
    "health",
    "home",
    "music",
    "real estate",
    "sport",
    "tourism",
    "toys",
    "other",
]


class Command(BaseCommand):
    help = "Create categories"

    def handle(self, *args, **options):
        for cat in CATEGORIES:
            if not Category.objects.filter(name=cat):
                Category.objects.create(name=cat)
