from faker import Faker
from random import randint


from auctions.models import Auction, User

fake = Faker("en-US")


def create_fake_user():
    """Generate new fake user and save to database."""
    return User.objects.create_user(
            username=f'user_1_{fake.safe_color_name()}',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=f'person1@example.com',
            password=f'alaMAkota1!',
            address=fake.address()
        )


def create_fake_auction():
    """Generate new fake auction and save to database."""
    return Auction.objects.create(
        title=fake.sentence(nb_words=3),
        description=fake.sentence(nb_words=10),
        min_price=randint(1, 50) - (randint(1, 100)/100),
        owner=create_fake_user()
    )


def create_n_fake_users(n):
    """Generate 'n' new fake users and save to database."""
    for i in range(n):
        User.objects.create_user(
            username=f'user_{i}_{fake.safe_color_name()}',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=f'person{i}@example.com',
            password=f'alaMAkota{i}!',
            address=fake.address()
        )
    return User.objects.all()