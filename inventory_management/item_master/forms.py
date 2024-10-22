from django import forms
from .models import Item
from .models import BrandMaster

CATEGORY_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Stationary', 'Stationary'),
    ('Clothing', 'Clothing'),
    ('Home Goods', 'Home Goods'),
    ('Books', 'Books'),
    ('Other', 'Other'),
]

class ItemForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)

    class Meta:
        model = Item
        fields = ['item_name','brand', 'category', 'unit_price', 'image']  

class BrandForm(forms.ModelForm):
    class Meta:
        model = BrandMaster
        fields = ['brand_name'] 