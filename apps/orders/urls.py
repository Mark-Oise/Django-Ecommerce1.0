from django.urls import path
from .views import create_order, get_order_items, update_order_summary

app_name = 'orders'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('get_order_items', get_order_items, name='get_order_items'),
    path('update_order_summary', update_order_summary, name='update_order_summary')
]
