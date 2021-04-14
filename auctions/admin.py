from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Auction, Bid, Category, Comment, User

admin.site.register(User, UserAdmin)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Comment)

