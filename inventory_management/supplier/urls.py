from django.urls import path
from .views import supplier_list

urlpatterns = [
    path('', supplier_list, name='supplier_list'),
]
