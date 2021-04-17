from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import View

from .forms import AuctionForm, BidForm
from .models import User, Auction, Bid


class IndexView(ListView):
    model = Auction
    queryset = Auction.objects.filter(active=True)


class RegisterView(CreateView):
    model = User



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

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass

