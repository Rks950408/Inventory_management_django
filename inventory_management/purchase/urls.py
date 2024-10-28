from django.urls import path
from .views import purchase_list,purchase_item,stock_list,sale_list,sale_item
from .views import get_item_detls ,purchase_details
urlpatterns = [
    path('', purchase_list, name='purchase_list'),
    path('purchase/add/', purchase_item, name='purchase_item'),
    path('get_item_detls/', get_item_detls, name='get_item_detls'),
    # path('purchases/purchase/add/', purchase_item, name='purchase_item'),
    path('purchase/<int:purchase_id>/', purchase_details, name='purchase_details'),


# sale urls
    path('sale_list/', sale_list, name='sale_list'),
    path('sale_item/', sale_item, name='sale_item'),



    # stock report
    path('stock/', stock_list, name='stock_list'),

]
