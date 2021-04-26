from faker import Faker
from random import choice, randint


from auctions.models import Auction, Category, CustomUser
from auctions.management.commands.create_categories import CATEGORIES

fake = Faker("en-US")


def fake_user_data():
    """Generate a dict of user data"""
    nr = randint(1, 100)
    return {
        'username': f'user_{nr}_{fake.safe_color_name()}',
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': f'person{nr}@example.com',
        'password': 'strongPassword100%',
        'confirmation_password': 'strongPassword100%',
        'address': fake.address()
    }


def create_fake_user():
    """Generate new fake user and save to database."""
    user_data = fake_user_data()
    return CustomUser.objects.create_user(
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            address=user_data['address']
        )


def fake_auction_data():
    """Generate a dict of auction data"""
    for cat in CATEGORIES:
        if not Category.objects.filter():
            Category.objects.create(name=cat)
    return {
        'title': fake.sentence(nb_words=3),
        'description': fake.sentence(nb_words=3),
        'min_price': randint(1, 50) - (randint(1, 100)/100),
        'category': choice(Category.objects.all()),
        'owner': create_fake_user()
    }


def create_fake_auction():
    """Generate new fake auction and save to database."""
    auction_data = fake_auction_data()
    fake_auction = Auction.objects.create(
        title=auction_data['title'],
        description=auction_data['description'],
        min_price=auction_data['min_price'],
        owner=auction_data['owner']
    )
    fake_auction.category.set((auction_data['category'], ))
    fake_auction.save()
    return fake_auction


def create_n_fake_users(n):
    """Generate 'n' new fake users and save to database."""
    for i in range(n):
        CustomUser.objects.create_user(
            username=f'user_{i}_{fake.safe_color_name()}',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=f'person{i}@example.com',
            password=f'alaMAkota{i}!',
            address=fake.address()
        )
    return CustomUser.objects.all()
