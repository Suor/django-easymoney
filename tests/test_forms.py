from django.forms import ModelForm

from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product


def test_post(rf):
    req = rf.post('/', {'price': '2.12'})
    form = ProductForm(req.POST)
    obj = form.save(commit=False)
    assert obj.price == 2.12


def test_edit():
    p = Product(price=2.34)
    form = ProductForm(instance=p)

    html = form['price'].as_widget()
    assert '2.34' in html
    assert '$2.34' not in html
