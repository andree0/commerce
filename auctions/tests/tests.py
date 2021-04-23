import pytest

from auctions.models import Auction


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
