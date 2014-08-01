Django-EasyMoney
================

An easy to use money field for Django.
Handles type conversions and arithmetic seamlessly.


Requirements
------------

Python 2.7, Django 1.6.


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


TODO
----

- form field
- widget
