from django.contrib import admin
from .models import AuctionListings, Bid, Comments

# Register your models here.
admin.site.register(AuctionListings)
admin.site.register(Bid)
admin.site.register(Comments)