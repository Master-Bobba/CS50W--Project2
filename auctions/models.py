from tkinter import CASCADE
from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #might need to add references here to the users Activelistings and bids
    pass


class AuctionListing(models.Model):
    #owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    starting_bid = models.IntegerField()
    image_url = models.URLField(unique= True, blank=True)
    category = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"Bid for {self.title} starting at {self.starting_bid}"

class Bid(models.Model):
    #listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    #current_price = models.IntegerField(blank = True)
    #bidder= models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    pass

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.username.first_name} {self.username.last_name} commented on {self.listing}: {self.content}"
