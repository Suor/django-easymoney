from __future__ import absolute_import

import sys
from decimal import Decimal, ROUND_HALF_UP

import babel.core
import babel.numbers
from django import forms
from django.db import models
from django.conf import settings
import six


__all__ = ['Money', 'MoneyField']


# Set up money arithmetic
def _to_decimal(amount):
    if isinstance(amount, Decimal):
        return amount
    elif isinstance(amount, float):
        return Decimal.from_float(amount)
    else:
        return Decimal(amount)


def _make_unary_operator(name):
    method = getattr(Decimal, name, None)
    # NOTE: current context would be used anyway, so we can just ignore it.
    #       Newer pythons don't have that, keeping this for compatability.
    return lambda self, context=None: self.__class__(method(self))


def _prepare_operand(self, other):
    try:
        return _to_decimal(other)
    except:
        raise TypeError(
            "Cannot do arithmetic operation between "
            "{} and {}.".format(repr(self), repr(other))
        )


def _make_binary_operator(name):
    method = getattr(Decimal, name, None)
    def binary_function(self, other, context=None):
        other = _prepare_operand(self, other)
        return self.__class__(method(self, other))
    return binary_function


def format_currency(number, currency, format, locale=babel.numbers.LC_NUMERIC,
                    force_frac=None, format_type='standard'):
    """Same as ``babel.numbers.format_currency``, but has ``force_frac``
    argument instead of ``currency_digits``.

    If the ``force_frac`` argument is given, the argument is passed down to
    ``pattern.apply``.
    """
    locale = babel.core.Locale.parse(locale)
    if format:
        pattern = babel.numbers.parse_pattern(format)
    else:
        try:
            pattern = locale.currency_formats[format_type]
        except KeyError:
            raise babel.numbers.UnknownCurrencyFormatError(
                "%r is not a known currency format type" % format_type)
    if force_frac is None:
        fractions = babel.core.get_global('currency_fractions')
        try:
            digits = fractions[currency][0]
        except KeyError:
            digits = fractions['DEFAULT'][0]
        frac = (digits, digits)
    else:
        frac = force_frac
    return pattern.apply(number, locale, currency=currency, force_frac=frac)


# Data class

class Money(Decimal):
    # Class settings to override in descendants
    CODE = getattr(settings, 'CURRENCY_CODE', 'USD')
    FORMAT = getattr(settings, 'CURRENCY_FORMAT', None)
    LOCALE = getattr(settings, 'CURRENCY_LOCALE', 'en_US')
    DECIMAL_PLACES = getattr(settings, 'CURRENCY_DECIMAL_PLACES', 2)
    MIN_DECIMAL_PLACES = 2

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
        string = self._format_currency(Decimal(self))
        if six.PY2:
            return string.encode('utf-8')
        return string

    @classmethod
    def _format_currency(cls, number):
        return format_currency(
            number=number,
            currency=cls.CODE,
            format=cls.FORMAT,
            locale=cls.LOCALE,
            force_frac=(cls.MIN_DECIMAL_PLACES, cls.DECIMAL_PLACES)
        )

    def __format__(self, format_spec):
        if format_spec in {'', 's'}:
            formatted = six.text_type(self)
        else:
            formatted = format(Decimal(self), format_spec)

        if isinstance(format_spec, six.binary_type):
            return formatted.encode('utf-8')
        else:
            return formatted

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, Decimal.__str__(self))

    def __eq__(self, other):
        if isinstance(other, Money):
            return Decimal.__eq__(self, other)
        elif isinstance(other, six.integer_types + (float, Decimal)):
            return Decimal.__eq__(self, self._sanitize(other))
        else:
            return False

    # for Python 3:
    # need to re-define __hash__ because we defined __eq__ above
    # https://docs.python.org/3.5/reference/datamodel.html#object.%5F%5Fhash%5F%5F
    __hash__ = Decimal.__hash__

    # Special casing this, cause it have extra modulo arg
    def __pow__(self, other, modulo=None):
        other = _prepare_operand(self, other)
        return self.__class__(Decimal.__pow__(self, other, modulo))

    __abs__ = _make_unary_operator('__abs__')
    __pos__ = _make_unary_operator('__pos__')
    __neg__ = _make_unary_operator('__neg__')

    __add__ = _make_binary_operator('__add__')
    __radd__ = _make_binary_operator('__radd__')
    __sub__ = _make_binary_operator('__sub__')
    __rsub__ = _make_binary_operator('__rsub__')
    __mul__ = _make_binary_operator('__mul__')
    __rmul__ = _make_binary_operator('__rmul__')
    __floordiv__ = _make_binary_operator('__floordiv__')
    __rfloordiv__ = _make_binary_operator('__rfloordiv__')
    __truediv__ = _make_binary_operator('__truediv__')
    __rtruediv__ = _make_binary_operator('__rtruediv__')
    if hasattr(Decimal, '__div__'):
        __div__ = _make_binary_operator('__div__')
        __rdiv__ = _make_binary_operator('__rdiv__')
    __mod__ = _make_binary_operator('__mod__')
    __rmod__ = _make_binary_operator('__rmod__')
    __divmod__ = _make_binary_operator('__divmod__')
    __rdivmod__ = _make_binary_operator('__rdivmod__')
    __rpow__ = _make_binary_operator('__rpow__')

    def deconstruct(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__), \
               [Decimal.__str__(self)], {}


# Model field

class MoneyField(six.with_metaclass(models.SubfieldBase, models.DecimalField)):
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
