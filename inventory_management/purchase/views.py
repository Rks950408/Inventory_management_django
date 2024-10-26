from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PurchaseMaster, PurchaseDetails, Item
from supplier.models import Supplier
from item_master.models import BrandMaster
from django.utils import timezone
import datetime

def purchase_list(request):
    purchases = PurchaseMaster.objects.all()  
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

def purchase_item(request):
    suppliers = Supplier.objects.filter(status=1)
    item_dtls = Item.objects.filter(status=1)
    curr_date = datetime.datetime.today().strftime('%d-%m-%Y')

    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        invoice_no = request.POST.get('invoice_no')
        if not invoice_no:
            return JsonResponse({'error': 'Invoice number is required'}, status=400)

        try:
            invoice_date = datetime.datetime.strptime(request.POST["invoice_date"], '%d-%m-%Y').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format for invoice date'}, status=400)

        supplier_id = request.POST.get('supplier_name')
        if not supplier_id:
            return JsonResponse({'error': 'Supplier is required'}, status=400)

        supp = Supplier.objects.filter(status=1, id=supplier_id).first()
        if not supp:
            return JsonResponse({'error': 'Supplier not found'}, status=404)

        item_id = request.POST.get('item_id')
        print(f"Item ID: {item_id}")
        if not item_id:
            print(f"Item not dfgyuyfdg") 
            return JsonResponse({'error': 'Item is required'}, status=400)

        item = Item.objects.filter(status=1, id=item_id).first()  # Use first() to get a single item
        print(f"Item check item_id: {item_id}") 
        if not item:
            print(f"Item not dfgyuyfdg") 
            return JsonResponse({'error': 'Item not found'}, status=404)

        # Fetch additional details
        brand = request.POST.get('brand')
        price_str = request.POST.get('price', '').strip()
        quantity_str = request.POST.get('quantity', '').strip()

        # Validate price and quantity
        if not price_str:
            return JsonResponse({'error': 'Price is required'}, status=400)
        if not quantity_str:
            return JsonResponse({'error': 'Quantity is required'}, status=400)

        # Convert price and quantity to float and int respectively
        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid price or quantity format'}, status=400)

        print(f"Price: {price}, Quantity: {quantity}") 

        # Validate that price and quantity are valid
        if price <= 0:
            return JsonResponse({'error': 'Price must be greater than 0'}, status=400)
        if quantity <= 0:
            return JsonResponse({'error': 'Quantity must be greater than 0'}, status=400)

        # Calculate total amount
        total = price * quantity
        print(f"Total: {total}")  

        # Insert data into PurchaseMaster
        insert_purchase = PurchaseMaster.objects.create(
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            supplier=supp,
            total_amount=total,
            datetime=timezone.now(),
            status=True
        )

        if insert_purchase:
            # Insert data into PurchaseDetails
            PurchaseDetails.objects.create(
                item=item,
                brand_name=brand,
                price=price,
                quantity=quantity,
                amount=total,
                datetime=timezone.now(),
                status=True,
                purchase_master=insert_purchase
            )

        return redirect('purchase_list')

    return render(request, 'purchase/add_purchase.html', {
        'suppliers': suppliers,
        'item_dtls': item_dtls,
        'curr_date': curr_date
    })


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
