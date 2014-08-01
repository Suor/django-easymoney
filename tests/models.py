from django.db import models

from easymoney import MoneyField


class Product(models.Model):
    price = MoneyField()
