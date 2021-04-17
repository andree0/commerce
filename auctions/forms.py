from django import forms
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator
)

from .models import Auction, Bid, User


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error(None, 'Podaj poprawny login lub hasło')

    def login(self, request):
        user = authenticate(**self.cleaned_data)
        return login(request, user)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[
        CommonPasswordValidator,
        MinimumLengthValidator,
        NumericPasswordValidator,
        UserAttributeSimilarityValidator
    ])
    confirmation_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'address')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirmation_password']:
            self.add_error('confirmation_password', "Hasła nie są identyczne !")
        if get_user_model().objects.filter(username=cleaned_data['username']):
            self.add_error('username', "Użytkownik o podanej nazwie już istnieje !")
        if get_user_model().objects.filter(email=cleaned_data['email']):
            self.add_error('email', "Użytkownik o podanym emailu już istnieje !")

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
        fields = ('price', )
