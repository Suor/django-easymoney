from __future__ import absolute_import
from django.db import models

from easymoney import MoneyField, Money


class Product(models.Model):
    price = MoneyField()


class Option(models.Model):
    price = MoneyField(choices=[(Money(0), Money(0)), (Money(0.5), Money(0.5))],
                       blank=True, null=True)


class GameMoney(Money):
    DECIMAL_PLACES = 0
    FORMAT = '# points'

class GameMoneyField(MoneyField):
    MONEY_CLASS = GameMoney

class Game(models.Model):
    prize = GameMoneyField()
