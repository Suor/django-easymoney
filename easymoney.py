import sys
from decimal import Decimal, ROUND_HALF_UP

from babel.core import Locale
from babel.numbers import parse_pattern
from django import forms
from django.db import models
from django.conf import settings


__all__ = ['Money', 'MoneyField']


# Data class

class Money(Decimal):
    # Class settings to override in descendants
    CODE = getattr(settings, 'CURRENCY_CODE', 'USD')
    FORMAT = getattr(settings, 'CURRENCY_FORMAT', None)
    LOCALE = getattr(settings, 'CURRENCY_LOCALE', 'en_US')
    DECIMAL_PLACES = getattr(settings, 'CURRENCY_DECIMAL_PLACES', 2)

    def __new__(cls, amount):
        return Decimal.__new__(cls, cls._sanitize(amount))

    @classmethod
    def _sanitize(cls, amount):
        if isinstance(amount, cls):
            return amount
        quant = Decimal('0.1') ** cls.DECIMAL_PLACES
        return _to_decimal(amount).quantize(quant, rounding=ROUND_HALF_UP)

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

    def __unicode__(self):
        return self._format_currency(Decimal(self))

    def __str__(self):
        return unicode(self).encode('utf-8')

    @classmethod
    def _format_currency(cls, number):
        locale = Locale.parse(cls.LOCALE)
        format = cls.FORMAT or locale.currency_formats['standard']
        pattern = parse_pattern(format)
        pattern.frac_prec = (2, cls.DECIMAL_PLACES)
        return pattern.apply(number, locale, currency=cls.CODE)

    def __format__(self, format_spec):
        if format_spec in {'', 's'}:
            formatted = unicode(self)
        else:
            formatted = format(Decimal(self), format_spec)

        if isinstance(format_spec, str):
            return formatted.encode('utf-8')
        else:
            return formatted

    def __repr__(self):
        return stdout_encode(u'Money(%s)' % self)

    def __eq__(self, other):
        if isinstance(other, Money):
            return Decimal.__eq__(self, other)
        elif isinstance(other, (int, long, float, Decimal)):
            return Decimal.__eq__(self, self._sanitize(other))
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

def _make_method(name):
    method = getattr(Decimal, name)
    return lambda self, other, context=None: \
        self.__class__(method(self, _to_decimal(other), context=context))

ops = 'add radd sub rsub mul rmul floordiv rfloordiv truediv rtruediv div rdiv mod rmod'
for op in ops.split():
    name = '__%s__' % op
    maker = make_compare if op in {'eq', 'ne'} else _make_method
    setattr(Money, name, maker(name))


# Model field

class MoneyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase
    MONEY_CLASS = Money

    # NOTE: we specify default value for max_digits for extra ease
    def __init__(self, verbose_name=None, name=None, max_digits=12, **kwargs):
        self.max_digits, self.decimal_places = max_digits, self.MONEY_CLASS.DECIMAL_PLACES
        models.Field.__init__(self, verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(MoneyField, self).deconstruct()
        del kwargs["decimal_places"]
        return name, path, args, kwargs

    def to_python(self, value):
        value = models.DecimalField.to_python(self, value)
        if value is None:
            return value

        return self.MONEY_CLASS(value)

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
