from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import PurchaseMaster, PurchaseDetails, Item, TempPurchaseDtls,SaleMaster,TempSalesDtls,SaleMaster,SaleDetails
from supplier.models import Supplier
from item_master.models import BrandMaster
from django.utils import timezone
import datetime 
from django.db.models import Sum
from datetime import date
import re

from django.shortcuts import render
from django.db import connection  

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
    return render(request, 'sale/sale_list.html',{ 'curr_date': curr_date,'sales':sales})


def sale_item(request):
    suppliers = Supplier.objects.filter(status=True)
    item_dtls = Item.objects.filter(status=True)
    curr_date = datetime.datetime.today().strftime('%d-%m-%Y')
    get_purchase = TempSalesDtls.objects.filter(status=True).order_by('id')

    if request.method == 'POST':
        if 'submit' in request.POST:
            print(request.POST)  
            
            invoice_date_str = request.POST['invoice_date']
            invoice_date = datetime.datetime.strptime(invoice_date_str, '%d-%m-%Y').date()

            sale_master = SaleMaster(
                invoice_no=request.POST['invoice_no'],
                invoice_date=invoice_date,
                customer=Supplier.objects.get(id=request.POST['supplier_name']),  # Correct field name
                total_amount=0.0,
                datetime=timezone.now()
            )
            sale_master.save()

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

            for item_id, fields in item_details.items():
                quantity = fields.get('quantity')
                price = fields.get('price')
                total = fields.get('total')

                if item_id and quantity and price and total:
                    sale_detail = SaleDetails(
                        sale_master=sale_master,
                        item_id=item_id,
                        quantity=int(quantity),
                        price=float(price),
                        amount=float(total),
                        brand_name = request.POST['brand_name_display']
                    )
                    sale_detail.save()
                    total_amount += float(total)
                    print(f"Saved SaleDetail: {sale_detail}")  # Confirm each detail saved

            sale_master.total_amount = total_amount
            sale_master.save()

            # Clear TempPurchaseDtls
            TempSalesDtls.objects.filter(status=True).delete()
            return redirect('sale_list')  # Redirect to a success page after saving

    context = {
        'suppliers': suppliers,
        'item_dtls': item_dtls,
        'curr_date': curr_date,
        'get_purchase': get_purchase,
    }
    return render(request, 'sale/sale_item.html', context)



def get_sale_detls(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id:
            return JsonResponse({'error': 'Item ID not provided'}, status=400)

        try:
            item = Item.objects.get(id=item_id)
            brand = BrandMaster.objects.filter(id=item.brand_id).first()

            # Calculate the total quantity purchased from PurchaseDetails for the selected item
            total_quantity = PurchaseDetails.objects.filter(item_id=item_id).aggregate(Sum('quantity'))['quantity__sum'] or 0
            sold_quantity = SaleDetails.objects.filter(item_id=item_id).aggregate(Sum('quantity'))['quantity__sum'] or 0
            # Calculate available quantity
            available_quantity = total_quantity - sold_quantity
            data = {
                'name': item.item_name,
                'price': item.unit_price,
                'brand_name': brand.brand_name if brand else None,
                'brand_id': brand.id if brand else None,
                'available_quantity': available_quantity  
            }
            return JsonResponse(data)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def sale_details(request, sale_id):
    sales = get_object_or_404(SaleMaster, id=sale_id)
    sale_details = SaleDetails.objects.filter(sale_master=sales)  # Use the object itself, not the ID
    return render(request, 'sale/sale_details.html', {
        'sale_master': sales,
        'sale_details': sale_details
    })

# stock report

def stock_list(request):
    item_dtls = Item.objects.filter(status=True)

    item_id = request.POST.get('item', None)  
    search_query = request.POST.get('search', '').strip() 

    # Build the base query
    base_query = '''
        WITH purchase_data AS (
            SELECT item_id, SUM(quantity) AS total_purchase_price
            FROM public.purchase_details
            GROUP BY item_id
        ),
        sale_data AS (
            SELECT item_id, SUM(quantity) AS total_sale_price
            FROM public.sale_details
            GROUP BY item_id
        )
        SELECT 
            item.item_name,
            COALESCE(sale_data.total_sale_price, 0) AS total_sale_price,
            COALESCE(purchase_data.total_purchase_price, 0) AS total_purchase_price,
            COALESCE(total_purchase_price, 0) - COALESCE(total_sale_price, 0) AS available_quantity
        FROM 
            public.item_master item
        LEFT JOIN 
            purchase_data ON item.id = purchase_data.item_id
        LEFT JOIN 
            sale_data ON item.id = sale_data.item_id
    '''

    # Add filtering conditions
    conditions = []
    if item_id:
        conditions.append(f'item.id = {item_id}')
    if search_query:
        conditions.append(f"item.item_name ILIKE '%{search_query}%'")  # Case-insensitive search

    if conditions:
        base_query += ' WHERE ' + ' AND '.join(conditions)

    # Execute your query
    with connection.cursor() as cursor:
        cursor.execute(base_query)
        stock_data = cursor.fetchall()  # Fetch all results

    # Pass stock_data to your template
    return render(request, 'report/stock_list.html', {
        'item_dtls': item_dtls,
        'stock_data': stock_data  # stock_data now contains the results from the query
    })
    
    
# details purchase and sales

def details_sale_prchse(request):
    # print(purchases)
    return render(request, 'report/details_stock.html')
