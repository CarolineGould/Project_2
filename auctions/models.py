from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    pass

# class Auction_Listing(models.Model):
#     create_date = models.DateTimeField(auto_now=True)
#     name = models.CharField(max_length=64)
#     about_listing = models.TextField(max_length=10000)
#     def __str__(self):
#     return f"{self.name}"

    
class Item(models.Model):
    id= models.AutoField(primary_key=True)
    title= models.CharField(max_length=64)
    description=models.CharField(max_length=1000)
    category= models.CharField (max_length=64)
    starting_bid= models.DecimalField(max_digits=6, decimal_places=2)
    # starting_bid= MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    image_URL=models.CharField (max_length=1000)
    is_closed =models.BooleanField(default= False)
    watchlist_users = models.ManyToManyField(User, blank=True, related_name="watchlist_items")


    def __str__(self):
        return f"{self.title}: {self.description}, {self.category}, {self.starting_bid}, {self.image_URL}"

class Bid(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    bid_amount=models.DecimalField(max_digits=6, decimal_places=2)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.id}: {self.item_id}, {self.create_date}, {self.bid_amount}, {self.item_id}"

class Comment(models.Model):    
    message= models.TextField()
    user_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name ="comments")
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name ="comments") 
    create_date= models.DateTimeField (auto_now_add= True)

# class WatchList (models.Model):
#     item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
#     user_id= models.ForeignKey(User, on_delete=models.CASCADE)

