from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import View

from .forms import AuctionForm, BidForm
from .models import User, Auction, Bid


def index(request):
    auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {'auctions': auctions})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class CreateNewAuctionView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = AuctionForm
    model = Auction
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        user = self.request.user

        form_kwargs = super(CreateNewAuctionView, self).get_form_kwargs()
        form_kwargs.update({
            "initial": {
                "owner": User.objects.get(username=user.username)
            }
        })
        return form_kwargs


class ListingPageView(View):
    template_name = 'auctions/listing_details.html'
    form_class = BidForm
    context = {}

    def get(self, request, auction_pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=auction_pk)
        self.context['auction'] = auction
        max_bid = Bid.objects.filter(auction=auction).aggregate(Max('price'))
        if max_bid['price__max'] is not None:
            self.context['current_price'] = max_bid['price__max']
            self.context['form'] = self.form_class({'price': max_bid['price__max'] + 0.1})
        else:
            self.context['form'] = self.form_class({'price': auction.min_price})

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass

