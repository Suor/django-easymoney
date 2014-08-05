from django.db import models

from easymoney import MoneyField, Money


class Product(models.Model):
    price = MoneyField()


class Option(models.Model):
    price = MoneyField(choices=[(Money(0), Money(0)), (Money(0.5), Money(0.5))])
