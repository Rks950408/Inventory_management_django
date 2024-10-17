from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm

def item_list(request):
    search_query = request.GET.get('search', '')
    items = Item.objects.all()

    if search_query:
        items = items.filter(item_name__icontains=search_query)

    return render(request, 'item_master/item_list.html', {'items': items, 'search_query': search_query})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Include request.FILES for image uploads
        if form.is_valid():
            form.save()
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
