from django.contrib import admin
from .models import PurchaseMaster, PurchaseDetails  # Import the correct models

# Register your models here.
admin.site.register(PurchaseMaster)
admin.site.register(PurchaseDetails)
