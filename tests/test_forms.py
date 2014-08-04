from django.forms import ModelForm

from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product


def test_form(rf):
    req = rf.post('/', {'price': '2.12'})
    form = ProductForm(req.POST)
    obj = form.save(commit=False)
    assert obj.price == 2.12
