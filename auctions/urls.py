from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", auth_views.LoginView.as_view(template_name='auctions/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("create_auction/", views.CreateNewAuctionView.as_view(), name="create_auction"),
    path("listing_details/<int:auction_pk>/", views.ListingPageView.as_view(), name="listing_details"),
    path("all_listings/", views.AllListingsView.as_view(), name="all_listings")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
