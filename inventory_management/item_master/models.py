from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

    def delete(self, *args, **kwargs):
        # Instead of deleting the object, just set status to False
        self.status = False
        self.save()
        
    class Meta:
        db_table = 'item_master'
        managed=False
        
