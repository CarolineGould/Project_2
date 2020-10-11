from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listings, name="category_listings"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("auctions/<id>", views.auctions, name="auctions"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path ("add_to_watch/<id>", views.add_to_watch, name= "add_to_watch"),
    path ("remove_from_watch/<id>", views.remove_from_watch, name= "remove_from_watch"),
    path ("close_listing/<id>", views.close_bid, name= "close_listing")                
        
    
]
