import sys
from decimal import Decimal, ROUND_HALF_UP

from django import forms
from django.db import models
from django.conf import settings

from babel.numbers import format_currency


__all__ = ['Money', 'MoneyField']


# Settings

CURRENCY_CODE = getattr(settings, 'CURRENCY_CODE', 'USD')
CURRENCY_LOCALE = getattr(settings, 'CURRENCY_LOCALE', 'en_US')


# Data class

class Money(Decimal):
    def __new__(cls, amount):
        return Decimal.__new__(Money, _sanitize(amount))

    # Support for pickling
    def __reduce__(self):
        return (self.__class__, (Decimal.__str__(self),))

    # Money is immutable
    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __float__(self):
        """Float representation."""
        return float(Decimal(self))

    def __str__(self):
        return format_currency(Decimal(self), CURRENCY_CODE, locale=CURRENCY_LOCALE)
    __unicode__ = __str__

    def __repr__(self):
        return stdout_encode(u'Money(%s)' % self)

    def __eq__(self, other):
        if isinstance(other, Money):
            return Decimal.__eq__(self, other)
        elif isinstance(other, (int, long, float, Decimal)):
            return Decimal.__eq__(self, _sanitize(other))
        else:
            return False

# Set up money arithmetic
def _to_decimal(amount):
    if isinstance(amount, Decimal):
        return amount
    elif isinstance(amount, float):
        return Decimal.from_float(amount)
    else:
        return Decimal(amount)

def _sanitize(amount):
    if isinstance(amount, Money):
        return amount
    return _to_decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def _make_method(name):
    method = getattr(Decimal, name)
    return lambda self, other, context=None: \
        Money(method(self, _to_decimal(other), context=context))

ops = 'add radd sub rsub mul rmul floordiv rfloordiv truediv rtruediv div rdiv mod rmod'
for op in ops.split():
    name = '__%s__' % op
    maker = make_compare if op in {'eq', 'ne'} else _make_method
    setattr(Money, name, maker(name))


# Model field

class MoneyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    # NOTE: we specify default value for max_digits for extra ease
    def __init__(self, verbose_name=None, name=None, max_digits=12, **kwargs):
        self.max_digits, self.decimal_places = max_digits, 2
        models.Field.__init__(self, verbose_name, name, **kwargs)

    def to_python(self, value):
        value = models.DecimalField.to_python(self, value)
        if value is None:
            return value

        return Money(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return Decimal(self.to_python(value))

    def formfield(self, **kwargs):
        defaults = {
            'form_class': MoneyFormField,
            'choices_form_class': MoneyChoiceField,
        }
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)


# Form fields

class MoneyFormField(forms.DecimalField):
    def prepare_value(self, value):
        return to_dec(value)


class MoneyChoiceField(forms.TypedChoiceField):
    def prepare_value(self, value):
        return to_dec(value)

    def __init__(self, *args, **kwargs):
        super(MoneyChoiceField, self).__init__(*args, **kwargs)
        self.choices = [(to_dec(k), v) for k, v in self.choices]


# Utils

def to_dec(value):
    return Decimal(value) if isinstance(value, Money) else value

def stdout_encode(u, default='UTF8'):
    if sys.stdout.encoding:
        return u.encode(sys.stdout.encoding)
    return u.encode(default)
