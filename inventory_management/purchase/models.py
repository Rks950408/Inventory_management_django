from django.db import models
from django.utils import timezone
from item_master.models import Item,BrandMaster
from supplier.models import Supplier

class PurchaseMaster(models.Model):
    id = models.AutoField(primary_key=True)     
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total_amount = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_no
    
    class Meta:
        db_table = 'purchase_master'
        managed = False


class PurchaseDetails(models.Model):
    id = models.AutoField(primary_key=True)  
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    purchase_master = models.ForeignKey(PurchaseMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_id} - {self.purchase_master_id}"
    
    class Meta:
        db_table = 'purchase_details'
        managed = False

class TempPurchaseDtls(models.Model):
    id = models.AutoField(primary_key=True)  
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    purchase_master = models.ForeignKey(PurchaseMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_id} - {self.purchase_master_id}"
    
    class Meta:
        db_table = 'tbl_temp_purchase_details'
        managed = False


# Sale Master Model 
class SaleMaster(models.Model):
    invoice_no=models.CharField(max_length=100 , blank=True , null=True)
    invoice_date=models.DateField(blank=True , null=True)
    customer=models.ForeignKey(Supplier ,on_delete=models.CASCADE)
    total_amount = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.invoice_no
    
    class Meta:
        db_table = 'sale_master'
        managed = False

# Sale Details Model
class SaleDetails(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    sale_master = models.ForeignKey(SaleMaster, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.item} - {self.sale_master}"
    
    class Meta:
        db_table = 'sale_details'
        managed = False
    
    
class TempSalesDtls(models.Model):
    id = models.AutoField(primary_key=True)  
    item_id = models.ForeignKey('item_master.Item', on_delete=models.CASCADE)  
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    sale_master_id = models.ForeignKey('purchase.SaleMaster', on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.item_id} - {self.sale_master_id}"
    
    class Meta:
        db_table = 'tbl_temp_sales_details'
        managed = False
