from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Auction, Bid, User
from .validators import validate_password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[validate_password, ]
    )
    confirmation_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password', 'confirmation_password', 'address', )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address (optional)'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username):
            self.add_error('username', "Username is already taken !")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email):
            self.add_error('email', "User with the given email already exists !")
        return email

    def clean_confirmation_password(self):
        confirmation_password = self.cleaned_data.get('confirmation_password')
        password = self.cleaned_data.get('password')
        if password:
            if confirmation_password != password:
                self.add_error('confirmation_password', "Passwords do not match !")
        return confirmation_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'min_price', 'category', 'image', 'owner',)
        widgets = {
            'category': forms.CheckboxSelectMultiple,
            'min_price': forms.NumberInput(attrs={'min': 1}),
            'owner': forms.HiddenInput()
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('price',)
