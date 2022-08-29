import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Comment, ListingBid


def index(request):
    return render(request, "auctions/index.html",{
        "listings": AuctionListing.objects.all(),
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

def new_listing(request):
    if request.method == "POST":
        new_owner = User.objects.get(username = request.user)
        new_title = request.POST["title"]
        new_description = request.POST["description"]
        new_starting_bid = int(request.POST["starting_bid"])
        new_image_url = request.POST["image_url"]
        new_category = request.POST["category"]

        listing=AuctionListing.objects.all()
        new_listing = AuctionListing(owner=new_owner, title = new_title, description=new_description, starting_bid=new_starting_bid, image_url=new_image_url, category=new_category)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/new_listing.html")

def listing(request, listing_id):
    
    listing = AuctionListing.objects.get(pk = listing_id)
    bids = listing.bids.all()

    if bids:    
        highest_bid = listing.starting_bid
        for bid in bids:
            if bid.bid_amount > highest_bid:
                highest_bid = bid.bid_amount
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": Comment.objects.filter(listing=listing_id),
            "price": ListingBid.objects.get(bid_amount = highest_bid).bid_amount,
            "number": len(bids)
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": Comment.objects.filter(listing=listing_id),
            "price": listing.starting_bid,
            "number": len(bids)
        })

def newcomment(request, listing_id):
    if request.method == "POST":
        username = User.objects.get(username = request.user)
        content = request.POST["content"]
        listing = AuctionListing.objects.get(pk = listing_id)

        new_comment = Comment(listing = listing, username=username, content=content)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def bid(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk = listing_id)
        new_bid_amount = request.POST["bid_amount"]
        new_bidder = User.objects.get(username = request.user)

        bids = listing.bids.all()
        highest_bid = listing.starting_bid
        number = len(bids)

        if bids:
            for bid in bids:
                if bid.bid_amount > highest_bid:
                    highest_bid = bid.bid_amount

            if int(new_bid_amount) > highest_bid:
                new_bid = ListingBid(bid_amount = new_bid_amount, bidder = new_bidder)
                new_bid.save()
                listing.bids.add(new_bid)
                listing.starting_bid = int(new_bid_amount)
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id, number)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": Comment.objects.filter(listing = listing_id),
                    "message": "Bid more than current bid",
                    "price": highest_bid,
                    "bid_number": number
                })
        else:
            if int(new_bid_amount) >= highest_bid:
                new_bid = ListingBid(bid_amount = new_bid_amount, bidder = new_bidder)
                new_bid.save()
                listing.bids.add(new_bid)
                listing.starting_bid = int(new_bid_amount)
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": Comment.objects.filter(listing = listing_id),
                    "message": "Bid more than current bid",
                    "price": listing.starting_bid,
                    "bid_number": number
                })

