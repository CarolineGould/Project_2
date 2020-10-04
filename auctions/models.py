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

class Item(models.Model):
    id= models.AutoField(primary_key=True)
    title= models.CharField(max_length=64)
    description=models.CharField(max_length=1000)
    category= models.CharField (max_length=64)
    starting_bid= models.DecimalField(max_digits=6, decimal_places=2)
    image_URL=models.CharField (max_length=1000)

    def __str__(self):
        return f"{self.title}: {self.description}, {self.category}, {self.starting_bid}, {self.image_URL}"
