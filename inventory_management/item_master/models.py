from django.db import models

class BrandMaster(models.Model):
    brand_name = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name.upper()  # Return uppercase for display

    def save(self, *args, **kwargs):
        self.brand_name = self.brand_name.upper()  # Convert brand_name to uppercase
        super().save(*args, **kwargs) 

    class Meta:
        db_table = 'brand_master'
        managed=False


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    # Foreign key to BrandMaster
    brand = models.ForeignKey(BrandMaster, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.item_name

    def delete(self, *args, **kwargs):
        self.status = False
        self.save()
        
    class Meta:
        db_table = 'item_master'
        managed=False
        

