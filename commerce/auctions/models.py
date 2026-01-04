from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=32)

    exact_name = models.CharField(max_length=64)

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)

    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)

    CATEGORY_CHOICES = [
        ("ELEC", "Electronics"),

        ("COMP", "Computers & Accessories"),

        ("PT", "Phones & Tablets"),

        ("HK", "Home & Kitchen"),

        ("FURN", "Furniture"),

        ("CLOTH", "Clothing & Accessories"),

        ("SHOES", "Shoes"),

        ("JW", "Jewelry & Watches"),

        ("SO", "Sports & Outdoors"),

        ("AUTO", "Automotive"),

        ("TOOL", "Tools & Home Improvement"),

        ("TG", "Toys & Games"),

        ("BM", "Books & Media"),

        ("MI", "Musical Instruments"),

        ("COLL", "Collectibles"),

        ("ART", "Art"),

        ("ANT", "Antiques"),

        ("HB", "Health & Beauty"),

        ("PS", "Pet Supplies"),

        ("RE", "Real Estate"),

        ("IB", "Industrial & Business"),

        ("FB", "Food & Beverages"),

        ("NULL", "No Category Listed"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="NULL")

    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')

    image_height = models.PositiveIntegerField(blank=True, null=True)
    image_width = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='listing_images/', height_field='image_height', width_field='image_width', blank=True, null=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=150)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)