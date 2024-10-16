from django.shortcuts import render

# Create your views here.
from .models import Purchase

def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})
