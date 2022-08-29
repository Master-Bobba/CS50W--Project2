from django.contrib import admin

from .models import User, AuctionListing, ListingBid, Comment
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(User)
admin.site.register(ListingBid)
admin.site.register(Comment)
