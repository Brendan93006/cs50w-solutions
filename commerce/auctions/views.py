from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListings, Bid, Comments

from decimal import Decimal, InvalidOperation

@login_required
def index(request):
    listings = AuctionListings.objects.filter(active=True)

    for listing in listings:
        listing.highest_bid = listing.bids.order_by("-price").first()
    
    return render(request, "auctions/index.html", { "listings": listings})


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

@login_required
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

@login_required
def create_listing(request):
    if request.method == "POST":

        title = request.POST.get("title")

        exact_name = request.POST.get("exact_name")

        if request.POST.get("category"):
            category = request.POST.get("category")
        else:
            category = "No Category Listed"

        if request.FILES.get("image"):
            image = request.FILES.get("image")
        else:
            image = None

        starting_bid = request.POST.get("starting_bid")


        if not title or not exact_name or not starting_bid:
            return render(request, "auctions/create.html", {"error": "All fields are required."})

        try:
            starting_bid = Decimal(starting_bid)
        except (InvalidOperation, TypeError):
            return render(request, "auctions/create.html", {"error": "Starting bid must be a valid number."})

        listing = AuctionListings(title=title, exact_name=exact_name, starting_bid=starting_bid, category=category, listed_by=request.user, image=image)

        listing.save()

        return redirect("index")
    
    return render(request, "auctions/create.html")

@login_required
def listing_view(request, listing_id):

    listing = get_object_or_404(AuctionListings, pk=listing_id, active=True)
    
    highest_bid = listing.bids.order_by("-price").first()

    is_in_watchlist = listing.watchers.filter(pk=request.user.pk).exists()

    if highest_bid:
        current_price = highest_bid.price
        highest_bidder = highest_bid.bidder
    else:
        current_price = listing.starting_bid
        highest_bidder = listing.listed_by

    if request.user == listing.listed_by:
        lister = request.user
    else:
        lister = None

    error = None

    if request.method == "POST":
        if request.POST.get("action") == "place_bid": 
            bid_amount = request.POST.get("bid_price", "").strip()  
            try:
                bid_amount = Decimal(bid_amount)
            except (InvalidOperation, TypeError):
                error = "Invalid bid amount."
            else:
                if bid_amount <= current_price:
                    error = "Your bid must be higher than the current price."
                else: 
                    Bid.objects.create(listing=listing, bidder=request.user, price=bid_amount)
                    current_price = Decimal(bid_amount)
        elif request.POST.get("action") == "add_comment":
            comment = request.POST.get("comment")
            commenter = request.user
            Comments.objects.create(listing=listing, comment=comment, commenter=commenter)
        elif request.POST.get("action") == "watchlist":
            if listing.watchers.filter(pk=request.user.pk).exists():
                listing.watchers.remove(request.user)
                is_in_watchlist = False
            else:
                listing.watchers.add(request.user)
                is_in_watchlist = True
        elif request.POST.get("action") == "close_listing":
            if lister:
                listing.active = False
                listing.save()
                return redirect("closed_listing", listing_id=listing.id)

    comments = Comments.objects.filter(listing=listing).values_list("comment", "commenter__username")
    
    num_bids = listing.bids.count()

    return render(request, "auctions/listing.html", { "listing": listing, "bid_price": current_price, "num_bids": num_bids, "error": error, "highest_bidder": highest_bidder, "user": request.user, "comments": comments, "is_in_watchlist": is_in_watchlist, "lister": lister})

@login_required
def categories_view(request):
    categories = AuctionListings.CATEGORY_CHOICES
    return render(request, "auctions/categories.html", { "categories": categories })        
        
@login_required
def category_listings(request, category):
    listings = AuctionListings.objects.filter(category=category, active=True)

    for listing in listings:
        highest_bid = listing.bids.order_by("-price").first()

    return render(request, "auctions/index.html", { "listings": listings, "highest_bid": highest_bid })

@login_required
def watchlist_listings(request):

    watcher_listings = request.user.watchlist.filter(active=True)

    for listing in watcher_listings:
        listing.highest_bid = listing.bids.order_by("-price").first()

    return render(request, "auctions/watchlist_listings.html", {"listings": watcher_listings})

@login_required
def closed_listing(request, listing_id):
    listing = get_object_or_404(AuctionListings, pk=listing_id, active=False)

    winning_bid = listing.bids.order_by("-price").select_related("bidder").first()

    if winning_bid:
        winner = winning_bid.bidder
    else:
        winner = None

    return render(request, "auctions/closed_listing.html", {"winner": winner, "listing": listing})



