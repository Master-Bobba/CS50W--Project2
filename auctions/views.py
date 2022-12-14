import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Comment, ListingBid


def index(request):
    return render(request, "auctions/index.html",{
        "listings": AuctionListing.objects.filter(winner = "")
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
    
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        
        if user in listing.watchers.all():
            watched = True
        else:
            watched = False
    else: 
        watched = False
    
    if bids:    
        highest_bid = listing.starting_bid
        for bid in bids:
            if bid.bid_amount > highest_bid:
                highest_bid = bid.bid_amount
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": Comment.objects.filter(listing=listing_id),
            "price": ListingBid.objects.get(bid_amount = highest_bid).bid_amount,
            "bid_number": len(bids),
            "watched": watched
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": Comment.objects.filter(listing=listing_id),
            "price": listing.starting_bid,
            "bid_number": len(bids),
            "watched": watched
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
            #add automatically to watchlist
            user = User.objects.get(username = request.user)
            if user not in listing.watchers.all():
                listing.watchers.add(user)
            else:
                pass

            if int(new_bid_amount) > highest_bid:
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

def categories(request): 
    listings = AuctionListing.objects.filter(winner = "")
    categories = []
    for listing in listings:
        if listing.category not in categories:
            categories.append(listing.category)
        if not listing.category and "Other" not in categories:
            categories.append("Other")
    
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

def opencategory(request, category):
        listings = AuctionListing.objects.filter(winner = "")
        categories = []

        for listing in listings:
            if listing.category not in categories:
                categories.append(listing.category)
            if not listing.category and "Other" not in categories:
                categories.append("Other")
        
        if category == "Other":
            listings = AuctionListing.objects.filter(category = "")
        else:
            listings = AuctionListing.objects.filter(category = category).filter(winner = "") 
            
        return render(request, "auctions/categories.html",{
            "categories": categories,
            "listings": listings
        })

def watchlist(request):
    user = User.objects.get(username = request.user)
    listings = AuctionListing.objects.filter(watchers = user)
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

def watch(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(username = request.user)
        listing = AuctionListing.objects.get(pk = listing_id)

        if user not in listing.watchers.all():
            listing.watchers.add(user)
        else:
            pass

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def notwatch(request, listing_id):
    if request.method == "POST":

        user = User.objects.get(username = request.user)
        listing = AuctionListing.objects.get(pk = listing_id)

        listing.watchers.remove(user)
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def close(request, listing_id):
    if request.method == 'POST':

        listing = AuctionListing.objects.get(pk = listing_id)

        bids = listing.bids.all()
        highest_bid = listing.starting_bid

        if bids:
            for bid in bids:
                if bid.bid_amount > highest_bid:
                    highest_bid = bid.bid_amount
        #get the winner of the auction
            winner = listing.bids.get(bid_amount = highest_bid).bidder
        else:
            winner = listing.owner

        listing.winner = winner.username
        listing.save()

        return HttpResponseRedirect(reverse("index"))

