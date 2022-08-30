from tkinter import CASCADE
from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    #might need to add references here to the users Activelistings and bids
    pass

class ListingBid(models.Model):
    #listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    bidder= models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Bid {self.id} by {self.bidder} of £{self.bid_amount}.00"
    
class AuctionListing(models.Model):
    owner = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=128, blank=False)
    starting_bid = models.IntegerField(default = "0")
    image_url = models.URLField(unique= True, default="https://media.istockphoto.com/vectors/no-image-available-sign-vector-id936182806?k=20&m=936182806&s=612x612&w=0&h=pTQbzaZhCTxWEDhnJlCS2gj65S926ABahbFCy5Np0jg=")
    category = models.CharField(max_length=64, blank=True)
    bids = models.ManyToManyField(ListingBid, blank=True, related_name="bids")
    watchers = models.ManyToManyField(User, blank=True, related_name = "watchers")
    winner = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.title} made by {self.owner}: bids £{self.bids}"

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.username.first_name} {self.username.last_name} commented on {self.listing}: {self.content}"
