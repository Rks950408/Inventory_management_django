from django import forms
from .models import Item

CATEGORY_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Home Goods', 'Home Goods'),
    ('Books', 'Books'),
    ('Other', 'Other'),
]

class ItemForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)

    class Meta:
        model = Item
        fields = ['item_name', 'category', 'unit_price', 'image']  
