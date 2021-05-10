import pytest

from django.utils.http import urlencode

from auctions.models import Auction, Bid, Comment, CustomUser, Watchlist
from auctions.tests.utils import fake_auction_data, fake_user_data


# Check status code 200 - method GET ---------------------------------------

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


# Check status code 302 - Found - Redirection - method GET ------------------

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


# Check status code 302 - Found - Redirection - method POST -----------------


@pytest.mark.django_db
def test_registration_user(client):
    users_before = CustomUser.objects.count()
    user_data = fake_user_data()
    response = client.post('/register/', data=user_data)
    assert response.status_code == 302
    assert CustomUser.objects.count() == users_before + 1


@pytest.mark.django_db
def test_create_auction(client, user):
    client.login(username=user.username, password="strongPassword100%")
    auctions_before = Auction.objects.count()
    auction_data = fake_auction_data()
    response = client.post('/create_auction/', data=auction_data)
    assert response.status_code == 302
    assert Auction.objects.count() == auctions_before + 1


@pytest.mark.skip
@pytest.mark.django_db
def test_add_to_watchlist(client, auction, rf, user):
    client.login(user=user.username, password="strongPassword100%")
    watchlist_before = Watchlist.objects.count()
    url = f'/listings_details/{auction.pk}/'
    request = rf.get(url)
    request.user = user
    response = client.post(url, data={
        'eye': 'add_to_watchlist',
        'request': request,
        'auction': auction.pk,
        'user': user.pk
    }, content_type="application/x-www-form-urlencoded")
    assert response.status_code == 200
    assert Watchlist.objects.count() == watchlist_before + 1
    assert response.context["is_watch"]


@pytest.mark.django_db
def test_add_comment(client, auction, user):
    client.login(user=user.username, password="strongPassword100%")
    url = f'/listings_details/{auction.pk}/'
    comment_before = Comment.objects.count()
    data = {
        'comment': True,
        'user': user.pk,
        'auction': auction.pk,
        'description': 'To jest komentarz testowy !'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Comment.objects.count() == comment_before + 1


@pytest.mark.django_db
def test_add_bid(client, auction, user):
    client.login(user=user.username, password="strongPassword100%")
    url = f'/listings_details/{auction.pk}/'
    bid_before = Bid.objects.count()
    data = {
        'add_bid': True,
        'user': user.pk,
        'auction': auction.pk,
        'price': 100
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Bid.objects.count() == bid_before + 1
    assert auction.owner != user
    assert response.context["auction"].current_price == 100


@pytest.mark.django_db
def test_close_auction(client, auction, user):
    client.login(user=user.username, password="strongPassword100%")
    url = f'/listings_details/{auction.pk}/'
    auction.owner = user
    active_auction_before = Auction.objects.filter(active=True).count()
    data = {
        'close_listings': True
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context["auction"].active is False
    assert Auction.objects.filter(active=True).count() == \
           active_auction_before - 1

