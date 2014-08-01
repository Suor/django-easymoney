from decimal import Decimal, ROUND_HALF_UP

from django.db import models


class Money(Decimal):
    def __init__(self, amount):
        self.amount = sanitize(amount)

    def __str__(self):
        return '$%s' % self.amount # TODO: use babel

    def __repr__(self):
        return 'Money(%s)' % self

# Set up money arithmetic
def sanitize(amount):
    return Decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def make_method(name):
    return lambda self, other: Money(getattr(self.amount, name)(sanitize(other)))

def make_compare(name):
    return lambda self, other: getattr(self.amount, name)(sanitize(other))

ops = 'eq ne add radd sub rsub mul rmul floordiv rfloordiv truediv rtruediv div rdiv mod rmod'
for op in ops.split():
    name = '__%s__' % op
    maker = make_compare if op in {'eq', 'ne'} else make_method
    setattr(Money, name, maker(name))


class MoneyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    # NOTE: we specify default value for max_digits for extra ease
    def __init__(self, verbose_name=None, name=None, max_digits=12, **kwargs):
        self.max_digits, self.decimal_places = max_digits, 2
        models.Field.__init__(self, verbose_name, name, **kwargs)

    def to_python(self, value):
        value = models.DecimalField.to_python(value)
        if value is None:
            return value

        return Money(value)
