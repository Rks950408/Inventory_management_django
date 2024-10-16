from django.db import models

# Create your models here.
from item_master.models import Item
from supplier.models import Supplier

class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

    def __str__(self):
        return f"Purchase of {self.item.name} from {self.supplier.name}"
