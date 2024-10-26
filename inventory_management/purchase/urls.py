from django.urls import path
from .views import purchase_list,purchase_item
from .views import get_item_detls 
urlpatterns = [
    path('', purchase_list, name='purchase_list'),
    path('purchase/add/', purchase_item, name='purchase_item'),
    path('get_item_detls/', get_item_detls, name='get_item_detls'),
    # path('purchases/purchase/add/', purchase_item, name='purchase_item'),
]
