import pytest

from auctions.models import User
from .utils import fake_auction_data, fake_user_data


# Check status code 200 - method GET ------------------------------------

@pytest.mark.django_db
def test_get_index_view(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_login_view(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_register_view(client):
    response = client.get('/register/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_create_auction_view(user, client):
    client.force_login(user)
    response = client.get('/create_auction/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_all_listings_view(client):
    response = client.get('/all_listings/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_watchlist_view(user, client):
    client.force_login(user)
    response = client.get('/watchlist/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_your_auctions_view(user, client):
    client.force_login(user)
    response = client.get('/your_auctions/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_your_auctions_view(auction, client):
    response = client.get(f'/listings_details/{ auction.pk }/')
    assert response.status_code == 200


# Check status code 302 - Found - Redirection ----------------------------

@pytest.mark.django_db
def test_get_logout_view(client):
    response = client.get('/logout/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_auction_to_login_view(client):
    response = client.get('/create_auction/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_watchlist_to_login_view(client):
    response = client.get('/watchlist/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_your_auctions_to_login_view(client):
    response = client.get('/your_auctions/')
    assert response.status_code == 302


# Check status code 201 - method POST ------------------------------------

# @pytest.mark.django_db
# def test_registration_user(client):
#     user_data = fake_user_data()
#     response = client.post('/register/', user_data)
#     assert response.status_code == 302
#     users_before = User.objects.count()
#     assert User.objects.count() == users_before + 1
#     for key, value in user_data.items():
#         assert key in response.data
#         if isinstance(value, list):
#             # Compare contents regardless of their order
#             assert len(response.data[key]) == len(value)
#         else:
#             assert response.data[key] == value

# @pytest.mark.django_db
# def test_get_create_auction_view(user, client):
#     client.force_login(user)
#     auction_data = fake_auction_data()
#     response = client.get('/create_auction/', auction_data)
#     assert response.status_code == 302
