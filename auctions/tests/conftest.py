import pytest

from django.test import Client

from auctions.models import Auction, User
from .utils import create_n_fake_users, create_fake_auction, create_fake_user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return create_fake_user()


@pytest.fixture
def auction():
    return create_fake_auction()


@pytest.fixture
def n_users():
    return create_n_fake_users(5)
