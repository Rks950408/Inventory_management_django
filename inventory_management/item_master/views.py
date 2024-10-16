from django.shortcuts import render, redirect  # Import redirect
from .models import Item
from .forms import ItemForm

def item_list(request):
    search_query = request.GET.get('search', '')
    items = Item.objects.all()

    if search_query:
        items = items.filter(name__icontains=search_query)

    return render(request, 'item_master/item_list.html', {'items': items, 'search_query': search_query})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Changed to match the URL pattern name for item list
    else:
        form = ItemForm()
    return render(request, 'item_master/add_item.html', {'form': form})

def dashboard(request):
    total_items = Item.objects.count()
    active_items = Item.objects.filter(status=1).count()
    inactive_items = Item.objects.filter(status=0).count()

    context = {
        'total_items': total_items,
        'active_items': active_items,
        'inactive_items': inactive_items,
    }

    return render(request, 'item_master/dashboard.html', context)
