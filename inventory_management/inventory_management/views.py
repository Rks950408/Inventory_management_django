from django.shortcuts import render
from item_master.models import Item  


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
