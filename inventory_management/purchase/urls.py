from django.urls import path
from .views import purchase_list,purchase_item, get_supplier_details

urlpatterns = [
    path('', purchase_list, name='purchase_list'),
    path('purchase/add/', purchase_item, name='purchase_item'),
    path('supplier/<int:supplier_id>/details/', get_supplier_details, name='get_supplier_details'),


]
