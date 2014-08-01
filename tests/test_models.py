from decimal import Decimal
import pytest

from .models import Product


pytestmark = pytest.mark.django_db


def test_save():
    p = Product()
    p.price = 3.14
    p.save()


def test_get():
    p = Product.objects.create(price=3.14)

    p2 = Product.objects.get(pk=p.pk)
    assert p2.price == p.price

    # coercing
    p2 = Product.objects.get(price=3.136)
    assert p2.pk == p.pk


def test_fetch():
    Product.objects.bulk_create([
        Product(price=2.78),
        Product(price=3.14),
        Product(price=3.78),
    ])

    assert list(Product.objects.filter(price__lt=3.5).values_list('price', flat=True)) \
        == [Decimal('2.78'), Decimal('3.14')]
