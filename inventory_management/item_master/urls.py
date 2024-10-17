from django.urls import path
from .views import item_list, dashboard, add_item
from . import views


urlpatterns = [
    path('', item_list, name='item_list'),
    path('dashboard/', dashboard, name='item_dashboard'),
    path('items/add/', add_item, name='add_item'),
     path('item/edit/<int:id>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:id>/', views.delete_item, name='delete_item'),
]
