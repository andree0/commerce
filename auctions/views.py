from decimal import Decimal

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

from .forms import AuctionForm, BidForm, RegisterForm
from .models import User, Auction, Bid


class AllListingsView(ListView):
    model = Auction
    extra_context = {'all': True}


class IndexView(ListView):
    model = Auction
    queryset = Auction.objects.filter(active=True)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'auctions/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        form.save()
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


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


class ListingsPageView(View):
    template_name = 'auctions/listings_details.html'
    form_class = BidForm
    context = {}

    def get(self, request, auction_pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=auction_pk)
        self.context['auction'] = auction
        if auction.current_price:
            form = self.form_class(initial={'user': request.user, 'auction': auction,
                                            'price': round(float(auction.current_price) + 0.01, 2)})
        else:
            form = self.form_class(initial={'user': request.user, 'auction': auction,
                                            'price': round(float(auction.min_price) + 0.01, 2)})
        self.context['form'] = form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=kwargs['auction_pk'])
        if request.POST.get('add_bid'):
            form = self.form_class(request.POST)
            if form.is_valid():
                new_bid = Bid.objects.create(**form.cleaned_data)
                new_bid.save()
                auction.get_current_price()
                auction.save()
                self.context['auction'] = auction
                self.context['form'] = self.form_class(initial={
                    'user': request.user,
                    'auction': auction,
                    'price': round(float(auction.current_price) + 0.01, 2)})
            else:
                self.context['form'] = form
        if request.POST.get('close_listings'):
            auction.active = False
            auction.save()

        return render(self.request, self.template_name, self.context)


