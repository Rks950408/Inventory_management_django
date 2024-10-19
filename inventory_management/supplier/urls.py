from django.urls import path
from .views import supplier_list,supplier_add

urlpatterns = [
    path('', supplier_list, name='supplier_list'),
    path('supplier/add/',supplier_add, name='supplier_add'),

]
