from decimal import Decimal

from django import forms


class MoneyWidget(forms.TextInput):
    def _format_value(self, value):
        return str(Decimal(value))
