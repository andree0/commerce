from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", auth_views.LoginView.as_view(
        template_name='auctions/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        next_page="/"), name="logout"),
    path("register/", views.RegisterView.as_view(),
         name="register"),
    path("create_auction/", views.CreateNewAuctionView.as_view(),
         name="create_auction"),
    path("listings_details/<int:auction_pk>/",
         views.ListingsPageView.as_view(), name="listings_details"),
    path("all_listings/", views.AllListingsView.as_view(),
         name="all_listings"),
    path("category/<str:category_name>/",
         views.CategoryListingsView.as_view(),
         name="category_listings"),
    path("watchlist/", views.WatchlistView.as_view(),
         name="watchlist"),
    path("your_auctions/", views.YourAuctionsView.as_view(),
         name="your_auctions"),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT
                      )
