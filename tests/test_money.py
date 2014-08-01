from decimal import Decimal

from easymoney import Money


def test_create():
    assert Money(3) == Decimal('3')

    assert Money(3.14) == Decimal('3.14')
    assert Money(3.141) == Decimal('3.14')
    assert Money(3.145) == Decimal('3.15')

    assert Money('3.14') == Decimal('3.14')
    assert Money('3.141') == Decimal('3.14')
    assert Money('3.145') == Decimal('3.15')

    assert Money(Decimal('3.14')) == Decimal('3.14')
    assert Money(Decimal('3.141')) == Decimal('3.14')
    assert Money(Decimal('3.145')) == Decimal('3.15')


def test_str():
    assert str(Money(3.14)) == '$3.14'
    assert str(Money(3)) == '$3.00'


def test_arithmetic():
    pi = Money(3.14)
    e = Money(2.78)

    assert pi == 3.14
    assert pi == Decimal('3.14')
    assert pi != 3
    assert Money(3) == 3

    assert pi + e == 5.92
    assert pi - e == 0.36


def test_int_arithmetic():
    pi = Money(3.14)

    assert pi + 1 == 4.14
    assert pi - 1 == 2.14
    assert pi * 2 == 6.28
    assert pi / 3 == 1.05


def test_float_arithmetic():
    pi = Money(3.14)

    assert pi + 0.2 == 3.34
    assert pi - 0.2 == 2.94
    assert pi * 0.2 == 0.63
    assert pi / 1.5 == 2.09

    assert pi + 0.005 == 3.15
    assert pi - 0.005 == 3.13
