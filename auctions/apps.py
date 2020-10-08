from django.apps import AppConfig
from djmoney.models.fields import MoneyField
from django.db import models


class AuctionsConfig(AppConfig):
    name = 'auctions'
