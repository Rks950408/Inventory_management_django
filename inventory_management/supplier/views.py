from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import SupplierForm
# Create your views here.
from .models import Supplier

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})

def supplier_add(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].upper()
            contact = form.cleaned_data['contact']

            if Supplier.objects.filter(name=name).exists():
                messages.error(request, "A supplier with this name already exists.")
            elif Supplier.objects.filter(contact=contact).exists():
                messages.error(request, "A supplier with this phone number already exists.")
            else:
                supplier = form.save(commit=False)
                supplier.name = name
                supplier.address = supplier.address.upper()
                supplier.save()
                messages.success(request, "Supplier added successfully.")
                return redirect('supplier_list')
                
    else:
        form = SupplierForm()

    return render(request, 'supplier/add_supplier.html', {'form': form})
# 