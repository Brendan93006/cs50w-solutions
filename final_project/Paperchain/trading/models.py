from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    base_currency = models.CharField(max_length=3, default="USD", choices=[("USD", "USD")])
    starting_equity = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    cash_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0)

class Asset(models.Model):
    symbol = models.CharField(max_length=9, unique=True, db_index=True)
    name = models.CharField(max_length=30)

class Market(models.Model):
    symbol = models.CharField(max_length=30, unique=True, db_index=True)
    base_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="base_markets")
    quote_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="quote_markets")
    is_active = models.BooleanField(default=True)

class PriceSnapshot(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="price_snapshots")
    price = models.DecimalField(max_digits=20, decimal_places=8)
    source = models.CharField(max_length=32, default="coinbase_spot")
    captured_at = models.DateTimeField(db_index=True, default=timezone.now)

class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="orders")
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="orders")
    
    BUY = "BUY"
    SELL = "SELL"

    SIDE_CHOICES = [
        (BUY, "Buy"),
        (SELL, "Sell")
    ]

    side = models.CharField(max_length=4, choices=SIDE_CHOICES)

    OPEN = "OPEN"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (OPEN, "Open"),
        (FILLED, "Filled"),
        (CANCELLED, "Cancelled")
    ]

    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=OPEN)

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    order_type = models.CharField(max_length=6, choices=[(MARKET, "market"), (LIMIT, "limit")], default=MARKET)

    limit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)

    quantity = models.DecimalField(max_digits=20, decimal_places=8)

    filled_quantity = models.DecimalField(default=0, max_digits=20, decimal_places=8)

    avg_fill_price = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=8)

    created_at = models.DateTimeField(auto_now_add=True)

class Trade(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="trades")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="trades")
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="trades")

    BUY = "BUY"
    SELL = "SELL"

    SIDE_CHOICES = [
        (BUY, "Buy"),
        (SELL, "Sell")
    ]

    side = models.CharField(max_length=4, choices=SIDE_CHOICES)

    quantity = models.DecimalField(max_digits=20, decimal_places=8)

    price = models.DecimalField(max_digits=20, decimal_places=8)

    fee = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    executed_at = models.DateTimeField(default=timezone.now,  db_index=True)

    price_snapshot = models.ForeignKey(PriceSnapshot, on_delete=models.PROTECT, related_name="trades")

