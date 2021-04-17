from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Auction, Bid, User


def validate_password(value):
    if value.isdigit():
        raise ValidationError("Password cannot contain only numbers !")
    if len(value) < 9:
        raise ValidationError("Password must be longer than 8 characters !")
    if value.isalnum() is False or value.isspace() is True:
        raise ValidationError("Password cannot contain  whitespace !")
    if value.isalpha():
        raise ValidationError("Password must contain one digit and one special character !")
    if value.islower():
        raise ValidationError("Password must contain one uppercase letter !")
    if value.isupper():
        raise ValidationError("Password must contain one lowercase letter !")


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

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data['confirmation_password']:
            self.add_error('confirmation_password', "Passwords do not match !")
        if get_user_model().objects.filter(username=cleaned_data['username']):
            self.add_error('username', "Username is already taken !")
        if get_user_model().objects.filter(email=cleaned_data['email']):
            self.add_error('email', "User with the given email already exists !")

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
            'min_price': forms.NumberInput(attrs={'min': 0}),
            'owner': forms.HiddenInput()
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('price',)
