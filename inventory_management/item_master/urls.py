from django.urls import path
from .views import item_list, dashboard, add_item

urlpatterns = [
    path('', item_list, name='item_list'),
    path('dashboard/', dashboard, name='item_dashboard'),
    path('items/add/', add_item, name='add_item'),
]
