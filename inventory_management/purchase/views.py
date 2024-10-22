from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PurchaseMaster, PurchaseDetails, Item  # Update the import to use the correct models
from supplier.models import Supplier

# Create your views here.

def purchase_list(request):
    purchases = PurchaseMaster.objects.all()  # Use PurchaseMaster instead of Purchase
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

def purchase_item(request):
    suppliers = Supplier.objects.filter(status=1)
    item_dtls = Item.objects.filter(status=1)
    return render(request, 'purchase/add_purchase.html', {'suppliers': suppliers, 'item_dtls': item_dtls})

def get_item_detls(request):
    item_id = request.GET.get('item_id')
    item = Item.objects.filter(id=item_id).first()
    if item:
        data = {
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
        }
    else:
        data = {'error': 'Item not found'}
    return JsonResponse(data)