Django-EasyMoney
================

An easy to use money field for Django.
Handles type conversions and arithmetic seamlessly.


Requirements
------------

Python 2.7 and 3.3+, Django 1.6+.


Installation
------------

::

    pip install django-easymoney


Overview
--------

.. code:: python

    from django.db import models
    from easymoney import MoneyField

    class MyModel(models.Model):
        price = MoneyField(default=3.14)
        other_price = MoneyField(default=1)


    obj = MyModel()
    print obj.price # -> $3.14

    # Money arithmetic
    obj.price + obj.other_price # $4.14

    # Mix with ints and floats
    obj.price + 1   # $4.14
    obj.price + 0.2 # $3.34

    # No partial cents or crazy floats
    obj.price / 3   # $1.05


Settings
--------

A primary use of easymoney is global currency defined in settings
with global formatting and precision. Here is how you do that:

.. code:: python

    # These are default settings, code and locales refer to ones used in babel library
    CURRENCY_CODE = 'USD'
    CURRENCY_LOCALE = 'en_US'
    CURRENCY_DECIMAL_PLACES = 2

    # This is optional, for cases when you want to use some fake currency
    CURRENCY_FORMAT = '# points'


Several currencies
------------------

One money field can't store different currencies, however, you can create different money classes and model fields for them:

.. code:: python

    from easymoney import Money, MoneyField

    class GameMoney(Money):
        # CODE = '...'
        # LOCALE = '...'
        DECIMAL_PLACES = 0
        FORMAT = '# points'

    class GameMoneyField(MoneyField):
        MONEY_CLASS = GameMoney

