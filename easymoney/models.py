from decimal import Decimal, ROUND_HALF_UP

from django.db import models

from .forms import MoneyInput


class Money(Decimal):
    def __new__(cls, amount):
        return Decimal.__new__(Money, _sanitize(amount))

    # Money is immutable
    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __float__(self):
        """Float representation."""
        return float(Decimal(self))

    def __str__(self):
        return '$%s' % Decimal(self) # TODO: use babel

    def __repr__(self):
        return 'Money(%s)' % self

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
            'widget': MoneyInput,
        }
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)

        # if self.choices:
        #     # Also copy-pasted from Field.formfield
        #     defaults = {
        #         'choices': self.choices,
        #         'coerce': self.coerce,
        #         'required': not self.blank,
        #         'label': capfirst(self.verbose_name),
        #         'help_text': self.help_text,
        #         'widget': forms.CheckboxSelectMultiple
        #     }
        #     defaults.update(kwargs)
        #     return TypedMultipleChoiceField(**defaults)
        # else:
