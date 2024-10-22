from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Purchase
from supplier.models import Supplier
# Create your views here.

def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

def purchase_item(request):
    suppliers = Supplier.objects.all()  # Fetch all suppliers
    return render(request, 'purchase/add_purchase.html', {'suppliers': suppliers})


def get_supplier_details(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        return JsonResponse({
            'address': supplier.address,  # Returning the address field
        })
    except Supplier.DoesNotExist:
        return JsonResponse({'error': 'Supplier not found'}, status=404)