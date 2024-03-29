from typing import Any, Dict
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.images import get_image_dimensions
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import View

from auctions.forms import AuctionForm, BidForm, CommentForm, RegisterForm
from auctions.models import Auction, Bid, Category, Comment, CustomUser, Watchlist


AUCTIONS_PAGINATE_BY = 10


class AllListingsView(ListView):
    model = Auction
    ordering = "-created"
    extra_context = {"all": True}
    paginate_by = AUCTIONS_PAGINATE_BY


class IndexView(ListView):
    model = Auction
    queryset = Auction.objects.filter(active=True).order_by("-created")
    extra_context = {"categories": Category.objects.all()}
    paginate_by = AUCTIONS_PAGINATE_BY


class CategoryListingsView(ListView):
    model = Auction
    paginate_by = AUCTIONS_PAGINATE_BY

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        category = Category.objects.get(name=self.kwargs["category_name"])
        return Auction.objects.filter(category=category, active=True).order_by("-created")


class WatchlistView(LoginRequiredMixin, ListView):
    model = Auction
    paginate_by = AUCTIONS_PAGINATE_BY
    extra_context = {"watchlist": True}

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        watchlist = Watchlist.objects.filter(user=self.request.user).values_list("auction")
        return Auction.objects.filter(pk__in=watchlist).order_by("-created")


class YourAuctionsView(LoginRequiredMixin, ListView):
    model = Auction
    paginate_by = AUCTIONS_PAGINATE_BY

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        return Auction.objects.filter(owner=self.request.user).order_by("-created")


class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = "auctions/register.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        form.save()
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


class CreateNewAuctionView(LoginRequiredMixin, CreateView):
    form_class = AuctionForm
    model = Auction
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        user = self.request.user

        form_kwargs = super(CreateNewAuctionView, self).get_form_kwargs()
        form_kwargs.update({"initial": {"owner": CustomUser.objects.get(username=user.username)}})
        return form_kwargs


class ListingsPageView(View):
    template_name = "auctions/listings_details.html"
    form_class = BidForm
    context: Dict[str, Any] = {}

    def get_bid_count(self, auction):
        """Adds to context 'bid_count' and 'all_bids'."""
        if Bid.objects.filter(auction=auction):
            self.context["bid_count"] = Bid.objects.filter(auction=auction).count() - 1
            self.context["all_bids"] = Bid.objects.filter(auction=auction).count()
        else:
            self.context["bid_count"] = 0
            self.context["all_bids"] = 0

    def get(self, request, auction_pk, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        auction = get_object_or_404(Auction, pk=auction_pk)

        try:
            img_width, img_height = get_image_dimensions(auction.image.file)
            self.context["img_width"] = img_width
            self.context["img_height"] = img_height
        except (
            ValueError,
            FileNotFoundError,
        ):
            pass

        self.context["auction"] = auction

        if request.user.is_authenticated:
            if Watchlist.objects.filter(user=request.user, auction=auction):
                self.context["is_watch"] = True
            else:
                self.context["is_watch"] = False
            try:
                win_bid = Bid.objects.filter(auction=auction).order_by("-price").first()
                self.context["winner"] = win_bid.user
            except (ValueError, AttributeError):
                pass
            form_comment = CommentForm(initial={"user": request.user, "auction": auction})
            self.context["form_comment"] = form_comment

        self.get_bid_count(auction)

        if auction.current_price:
            form = self.form_class(
                initial={
                    "user": request.user,
                    "auction": auction,
                    "price": round(float(auction.current_price) + 0.01, 2),
                }
            )
        else:
            form = self.form_class(
                initial={
                    "user": request.user,
                    "auction": auction,
                    "price": round(float(auction.min_price) + 0.01, 2),
                }
            )
        self.context["form"] = form

        self.context["comment_list"] = Comment.objects.filter(auction=auction).order_by("-pk")

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        auction = get_object_or_404(Auction, pk=kwargs["auction_pk"])

        if request.POST.get("eye") == "add_to_watchlist":
            Watchlist.objects.create(user=request.user, auction=auction)
            self.context["is_watch"] = True

        if request.POST.get("eye") == "delete_from_watchlist":
            if Watchlist.objects.filter(user=request.user, auction=auction):
                Watchlist.objects.get(user=request.user, auction=auction).delete()
                self.context["is_watch"] = False

        if request.POST.get("add_bid"):
            form = self.form_class(request.POST)
            if form.is_valid():
                new_bid = Bid.objects.create(**form.cleaned_data)
                new_bid.save()
                auction.get_current_price()
                auction.save()
                self.context["auction"] = auction
                self.context["form"] = self.form_class(
                    initial={
                        "user": request.user,
                        "auction": auction,
                        "price": round(float(auction.current_price) + 0.01, 2),
                    }
                )
            else:
                self.context["form"] = form

        if request.POST.get("close_listings"):
            auction.active = False
            auction.save()
        try:
            win_bid = Bid.objects.filter(auction=auction).order_by("-price").first()
            self.context["winner"] = win_bid.user
        except (ValueError, AttributeError):
            pass
        self.context["auction"] = auction

        if request.POST.get("comment"):
            form_comment = CommentForm(request.POST)
            if form_comment.is_valid():
                Comment.objects.create(**form_comment.cleaned_data)
                self.context["comment_list"] = Comment.objects.filter(auction=auction).order_by(
                    "-pk"
                )

        self.get_bid_count(auction)

        return render(self.request, self.template_name, self.context)
