import pytest
from urllib.parse import urlencode

from auctions.models import Auction, CustomUser
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
    client.login(username=user.username, password='strongPassword100%')
    response = client.get('/create_auction/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_all_listings_view(client):
    response = client.get('/all_listings/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_watchlist_view(user, client):
    client.login(username=user.username, password='strongPassword100%')
    response = client.get('/watchlist/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_your_auctions_view(user, client):
    client.login(username=user.username, password='strongPassword100%')
    response = client.get('/your_auctions/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_listings_details_view(auction, client):
    response = client.get(f'/listings_details/{auction.pk}/')
    assert response.status_code == 200


# Check status code 302 - Found - Redirection - method GET ----------------------------

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


# Check status code 302 - Found - Redirection - method POST ----------------------------

# @pytest.mark.django_db
# def test_registration_user(client):
#     users_before = CustomUser.objects.count()
#     user_data = urlencode(fake_user_data())
#     response = client.post('/register/', data=user_data,
#                            content_type="application/x-www-form-urlencoded")
#     assert response.status_code == 302
#     assert CustomUser.objects.count() == users_before + 1


@pytest.mark.django_db
def test_registration_user(client):
    users_before = CustomUser.objects.count()
    user_data = fake_user_data()
    response = client.post('/register/', data=user_data,
                           format='json')
    assert response.status_code == 302
    assert CustomUser.objects.count() == users_before + 1


# @pytest.mark.django_db
# def test_create_auction(user, client):
#     client.login(username=user.username, password="strongPassword100%")
#     auctions_before = Auction.objects.count()
#     auction_data = urlencode(fake_auction_data())
#     response = client.post('/create_auction/', data=auction_data,
#                            content_type="application/x-www-form-urlencoded")
#     assert response.status_code == 302
#     assert Auction.objects.count() == auctions_before + 1


@pytest.mark.django_db
def test_create_auction(user, client):
    client.login(username=user.username, password="strongPassword100%")
    auctions_before = Auction.objects.count()
    auction_data = fake_auction_data()
    response = client.post('/create_auction/', data=auction_data,
                           format='json')
    assert response.status_code == 302
    assert Auction.objects.count() == auctions_before + 1
