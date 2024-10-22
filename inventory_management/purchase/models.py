from django.db import models
from django.utils import timezone
from item_master.models import Item
from supplier.models import Supplier

# Purchase Master Model
class Purchase(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(default=timezone.now)
    entry_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'purchase_master'  # Custom table name

    def __str__(self):
        return f"Purchase of {self.item.item_name} from {self.supplier.name}"
