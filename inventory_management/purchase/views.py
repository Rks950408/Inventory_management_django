from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import PurchaseMaster, PurchaseDetails, Item, TempPurchaseDtls,SaleMaster
from supplier.models import Supplier
from item_master.models import BrandMaster
from django.utils import timezone
import datetime 
from datetime import date

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
    suppliers = Supplier.objects.filter(status=1)
    item_dtls = Item.objects.filter(status=1)
    curr_date = datetime.datetime.today().strftime('%d-%m-%Y')
    get_purchase = ''
    if request.method == 'POST':
        if 'addItemBtn' in request.POST:
            invoice_no = request.POST['invoice_no']
            invoice_date = datetime.datetime.strptime(request.POST["invoice_date"], '%d-%m-%Y').date()
            supplier_id = request.POST['supplier_name']
            supp = Supplier.objects.filter(status=1, id=supplier_id).first()
            item_id = request.POST['item_id']
            item = Item.objects.filter(status=1, id=item_id).first()  # Use first() to get a single item
            brand = request.POST['brand_name_display']
            price = float(request.POST.get('price', 0)) 
            quantity = int(request.POST.get('quantity', 0))  
        
            # Calculate total amount
            total_amount = price * quantity

            # Insert data into PurchaseMaster
            insert_purchase = PurchaseMaster.objects.create(
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                supplier=supp,
                total_amount=total_amount,
                datetime=timezone.now(),
                status=True
            )
            if insert_purchase:
                temp_tbl  = TempPurchaseDtls.objects.create(
                    item_id    = request.POST['item_id'],
                    brand_name = request.POST['brand'],
                    price      = request.POST['price'],
                    quantity   = request.POST['quantity'],
                    amount     = request.POST['total'],
                    datetime   = timezone.now(),
                    status     = True,
                    purchase_master = insert_purchase
                )
                
        get_purchase = TempPurchaseDtls.objects.filter(status=True).order_by('id')
        print('getquery',get_purchase)
        if 'submit' in request.POST:
            for temp_item in get_purchase:
                print('temp_item',temp_item)
                print(f"Adding item with ID: {temp_item.item.id} to PurchaseDetails")
                PurchaseDetails.objects.create(
                    item=temp_item.item,
                    brand_name=temp_item.brand_name,
                    price=temp_item.price,
                    quantity=temp_item.quantity,
                    amount=temp_item.amount,
                    datetime=timezone.now(),
                    status=True,
                    purchase_master=temp_item.purchase_master
                )

            TempPurchaseDtls.objects.filter(status=True).update(status=False)
            return redirect('purchase_list')


    return render(request, 'purchase/add_purchase.html', {
        'suppliers': suppliers,
        'item_dtls': item_dtls,
        'curr_date': curr_date,
        'get_purchase' :get_purchase
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

