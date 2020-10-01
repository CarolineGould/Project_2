from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class Auction_Listing(models.Model):
#     create_date = models.DateTimeField(auto_now=True)
#     name = models.CharField(max_length=64)
#     about_listing = models.TextField(max_length=10000)
#     def __str__(self):
#     return f"{self.name}"

# class Bid(models.Model):
#     create_date = models.DateTimeField(auto_now=True)
#     bid_amount=models.
#     max_bid=
    