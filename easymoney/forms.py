from decimal import Decimal

from django import forms


class MoneyInput(forms.NumberInput):
    def _format_value(self, value):
        return str(Decimal(value))
