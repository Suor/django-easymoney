from django.forms import ModelForm

from .models import Product, Option


class ProductForm(ModelForm):
    class Meta:
        model = Product

class OptionForm(ModelForm):
    class Meta:
        model = Option


def test_post(rf):
    req = rf.post('/', {'price': '2.12'})
    form = ProductForm(req.POST)
    obj = form.save(commit=False)
    assert obj.price == 2.12


def test_edit():
    p = Product(price=2.34)
    form = ProductForm(instance=p)

    html = form['price'].as_widget()
    assert 'type="number"' in html
    assert 'step="0.01"' in html
    assert '2.34' in html
    assert '$2.34' not in html


def test_select():
    # p = Product(price=2.34)
    form = OptionForm(instance=Option(price=0.5))

    html = form['price'].as_widget()
    assert html.startswith('<select')
    assert 'selected' in html
