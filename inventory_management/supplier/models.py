from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    # user_id = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'supplier_master'
        managed=False

