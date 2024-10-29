from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import PurchaseMaster, PurchaseDetails, Item, TempPurchaseDtls,SaleMaster
from supplier.models import Supplier
from item_master.models import BrandMaster
from django.utils import timezone
import datetime 
from datetime import date
import re

def purchase_details(request, purchase_id):
    purchase = get_object_or_404(PurchaseMaster, id=purchase_id)
    purchase_details = PurchaseDetails.objects.filter(purchase_master=purchase)  # Use the object itself, not the ID
    return render(request, 'purchase/purchase_details.html', {
        'purchase_master': purchase,
        'purchase_details': purchase_details
    })
def purchase_list(request):
    purchases = PurchaseMaster.objects.all()  
    # print(purchases)
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})
def purchase_item(request):
    suppliers = Supplier.objects.filter(status=True)
    item_dtls = Item.objects.filter(status=True)
    curr_date = datetime.datetime.today().strftime('%d-%m-%Y')
    get_purchase = TempPurchaseDtls.objects.filter(status=True).order_by('id')

    if request.method == 'POST':
        if 'submit' in request.POST:
            print(request.POST)  # Debug print to see the entire POST data
            
            invoice_date_str = request.POST['invoice_date']
            invoice_date = datetime.datetime.strptime(invoice_date_str, '%d-%m-%Y').date()

            purchase_master = PurchaseMaster(
                invoice_no=request.POST['invoice_no'],
                invoice_date=invoice_date,
                supplier_id=request.POST['supplier_name'],
                total_amount=0.0,
                datetime=timezone.now()
            )
            purchase_master.save()

            total_amount = 0
            # Regex pattern to match 'items[<item_id>][field]'
            item_pattern = re.compile(r'items\[(\d+)\]\[(\w+)\]')

            # Dictionary to temporarily hold item details
            item_details = {}

            # Extract item details from POST data
            for key, value in request.POST.items():
                match = item_pattern.match(key)
                if match:
                    item_id = match.group(1)  # Extract item_id
                    field_name = match.group(2)  # Extract field (quantity, price, total)
                    if item_id not in item_details:
                        item_details[item_id] = {}
                    item_details[item_id][field_name] = value

            # Create PurchaseDetails entries from parsed item details
            for item_id, fields in item_details.items():
                quantity = fields.get('quantity')
                price = fields.get('price')
                total = fields.get('total')

                if item_id and quantity and price and total:
                    # Create a new PurchaseDetails instance
                    purchase_detail = PurchaseDetails(
                        purchase_master=purchase_master,
                        item_id=item_id,
                        quantity=int(quantity),
                        price=float(price),
                        amount=float(total)
                    )
                    purchase_detail.save()
                    total_amount += float(total)
                    print(f"Saved PurchaseDetail: {purchase_detail}")  # Confirm each detail saved

            # Update the total_amount for PurchaseMaster
            purchase_master.total_amount = total_amount
            purchase_master.save()

            # Clear TempPurchaseDtls
            TempPurchaseDtls.objects.filter(status=True).delete()
            return redirect('purchase_list')  # Redirect to a success page after saving

    context = {
        'suppliers': suppliers,
        'item_dtls': item_dtls,
        'curr_date': curr_date,
        'get_purchase': get_purchase,
    }
    return render(request, 'purchase/add_purchase.html', context)
def get_item_detls(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id:
            return JsonResponse({'error': 'Item ID not provided'}, status=400)

        try:
            item = Item.objects.get(id=item_id)
            brand = BrandMaster.objects.filter(id=item.brand_id).first()
            data = {
                'name': item.item_name,
                'price': item.unit_price,
                'brand_name': brand.brand_name if brand else None,
                'brand_id': brand.id if brand else None  
            }
            return JsonResponse(data)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# sale master


def sale_list(request):
    sales = SaleMaster.objects.all()  
    # print(purchases)
    curr_date = datetime.datetime.today().strftime('%d-%m-%Y')
    return render(request, 'sale/sale_list.html',{ 'curr_date': curr_date})


def sale_item(request):
    return render(request, 'sale/sale_item.html')


# stock report


def stock_list(request):
    return render(request, 'report/stock_list.html')

