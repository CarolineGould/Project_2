from django.contrib import admin
from .models import Item, Bid, Comment  

# Register your models here.
admin.site.register(Item),
admin.site.register(Bid),
admin.site.register(Comment)