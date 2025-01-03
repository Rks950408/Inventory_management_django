from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.contrib import messages
from .models import BrandMaster
from .forms import BrandForm

def item_list(request):
    search_query = request.GET.get('search', '')
    items = Item.objects.filter(status=True)  # Filter items with status=True

    if search_query:
        items = items.filter(item_name__icontains=search_query)

    return render(request, 'item_master/item_list.html', {'items': items, 'search_query': search_query})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False) 
            item.status = True  

            item.item_name = item.item_name.upper()
            item.category = item.category.upper()
            item.brand = form.cleaned_data['brand']
            item.unit_price = form.cleaned_data['unit_price']
            item.image = request.FILES.get('image')

            if Item.objects.filter(item_name__iexact=item.item_name).exists():
                messages.error(request, f'Item "{form.cleaned_data["item_name"]}" already exists!')
            else:
                item.save()  
                messages.success(request, 'Item added successfully!')
                return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'item_master/add_item.html', {'form': form})

def dashboard(request):
    total_items = Item.objects.count()
    active_items = Item.objects.filter(status=True).count()
    inactive_items = Item.objects.filter(status=False).count()

    context = {
        'total_items': total_items,
        'active_items': active_items,
        'inactive_items': inactive_items,
    }

    return render(request, 'item_master/dashboard.html', context)

# Edit Item by ID
def edit_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')  
    else:
        form = ItemForm(instance=item)

    return render(request, 'item_master/edit_item.html', {'form': form, 'item': item})

# Delete Item by ID
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':  
        item.delete()
        return redirect('item_list')  

    return render(request, 'item_master/delete_item.html', {'item': item})


def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand_name = form.cleaned_data['brand_name'].upper()  # Get the brand name in uppercase
            
            # Check if the brand already exists
            if BrandMaster.objects.filter(brand_name__iexact=brand_name).exists():
                messages.error(request, f'Brand "{brand_name}" already exists!')
            else:
                form.save()  
                messages.success(request, 'Brand added successfully!')
                form = BrandForm()  # Reset the form for a new entry
    else:
        form = BrandForm()

    return render(request, 'item_master/add_brand.html', {'form': form})
