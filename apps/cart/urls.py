from django.urls import path
from .views import cart_view, add_to_cart, increase_item_quantity, decrease_item_quantity, hx_cart_button, \
    update_cart_summary, remove_cart_item, get_cart_items, hx_empty_cart

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('increase/<slug:product_slug>/', increase_item_quantity, name='increase_item_quantity'),
    path('decrease/<slug:product_slug>/', decrease_item_quantity, name='decrease_item_quantity'),
    path('remove/<slug:product_slug>/', remove_cart_item, name='remove_cart_item'),
    path('update', update_cart_summary, name="update_cart_summary"),
    path('get_cart_items', get_cart_items, name='get_cart_items'),
    path('hx_cart_button', hx_cart_button, name='hx_cart_button'),
    path('empty_cart', hx_empty_cart, name='hx_empty_cart'),
]
