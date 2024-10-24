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
      
        invoice_no = request.POST['invoice_no']
        print(invoice_no)
        invoice_date =datetime.datetime.strptime(request.POST["invoice_date"], '%d-%m-%Y').date() 
        print(invoice_date)
        supplier_id = request.POST['supplier_name']  
        supp = Supplier.objects.filter(status=1, id=supplier_id).first()
        item_id = request.POST['item_name']  
        item = Item.objects.filter(id=item_id).first() 

        brand = request.POST['brand']  

        price = float(request.POST['price'])  
        quantity = int(request.POST['quantity'])  
        total = price * quantity  

        
        insert_purchase = PurchaseMaster.objects.create(
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            supplier=supp,
            total_amount=total,  
            datetime=timezone.now(),
            status=True
        )

       
        if insert_purchase:
            
            insert_purchase_dtls = PurchaseDetails.objects.create(
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
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

        brand = BrandMaster.objects.filter(id=item.brand_id).first() 

        data = {
            'name': item.item_name,  
            'price': item.unit_price,  
            'brand_name': brand.brand_name if brand else None  
        }

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
