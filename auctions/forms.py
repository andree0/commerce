from django import forms

from .models import Auction, Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'min_price', 'category', 'image', 'owner',)
        widgets = {
            'category': forms.CheckboxSelectMultiple,
            'min_price': forms.NumberInput(attrs={'min': 0}),
            'owner': forms.HiddenInput()
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('price', )
