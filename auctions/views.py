from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from .models import Item, User, Comment, Bid

class CommentForm(ModelForm):
    class Meta:
        model= Comment
        fields = ["message"]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_amount"]


def index(request):
    auction_items=Item.objects.all() 
    for item in auction_items:
        item.price= get_min_price(item.id)
    return render(request, "auctions/index.html", {
        "entries": auction_items
    })

def auctions(request,id):
    print (id)
    auction_item = Item.objects.get(pk=id)
    current_price= get_min_price(id)
    min_bid= current_price +1

    return render(request, "auctions/listing.html", {
        "listing": auction_item,
        "min_bid": min_bid,
        "current_price": current_price,
        "comment_form": CommentForm(initial={
            "user_id": request.user.username
        }),
        
        "bid_form": BidForm(initial={
            "user_id": request.user.username
        })
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
   
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "category", "starting_bid", "image_URL", "seller"]

@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html",{
            "form" : ItemForm()
        })
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/create_listing.html",{
            "form" : ItemForm()
        })

def categories(request):    
    categories = list(set([listing.category for listing in Item.objects.all() if listing.category]))
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category):
    return render(request, "auctions/category_list.html", {
        "listings": Item.objects.filter(category=category),
        "title": f'Active listings under "{category}"'
    })

@login_required
def bid(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        bidded_amount = request.POST["bid_amount"]
        bid= Bid(user_id=request.user, item_id=Item.objects.get(pk=item_id), bid_amount = bidded_amount)
        bid.save()
    return HttpResponseRedirect(reverse('auctions' , args =[item_id]))

@login_required
def comment(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        message_content = request.POST["message"]
        comment= Comment(user_id=request.user, item_id=Item.objects.get(pk=item_id), message=message_content)
        comment.save()
    return HttpResponseRedirect(reverse('auctions' , args =[item_id]))

def get_min_price(id):
    list_bids=Bid.objects.filter(item_id=id).order_by("-bid_amount")
    if len(list_bids) > 0:
        return list_bids[0].bid_amount
    bid_item = Item.objects.get(pk=id)
    return bid_item.starting_bid  

@login_required
def add_to_watch(request,id):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        assert request.user.is_authenticated
        user = request.user
        listing = Item.objects.get(pk=id)
        if not user.watchlist_items.filter(pk=id).exists():
            user.watchlist_items.add(listing)
    return HttpResponseRedirect(reverse('auctions' , args =[item_id]))

@login_required
def remove_from_watch(request,id):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        assert request.user.is_authenticated
        user = request.user
        listing = Item.objects.get(pk=id)
        if user.watchlist_items.filter(pk=id).exists():
            user.watchlist_items.remove(listing)
       
    return HttpResponseRedirect(reverse('auctions' , args =[item_id]))

def watch_list (request):
    watch_items= request.user.watchlist_items.all()
    return render(request, "auctions/watch_list.html", {
        "listings": watch_items,
        "title": "Watchlist Items",

    })
@login_required
def close_bid(request):
    if request.method =="POST":
        item_id = request.POST["item_id"]
        if request.user_id == Item.objects.filter(id=item_id).get(seller):
            print(":HEREE")
            Item.objects.filter(id=item_id).update(is_closed=True)
    
    return HttpResponseRedirect(reverse('auctions' , args =[item_id]))
