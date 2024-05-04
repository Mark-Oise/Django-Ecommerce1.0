from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.sessions.models import Session
from .models import Cart, CartItem
from ..products.models import Product
from django.conf import settings


# Create your views here.


def get_cart(request):
    # Get the cart from the session
    cart_id = request.session.get(settings.CART_SESSION_ID)

    # If the cart doesn't exist in the session, create a new one
    if not cart_id:
        cart = Cart.objects.create()
        request.session[settings.CART_SESSION_ID] = cart.id
    else:
        cart = Cart.objects.get(id=cart_id)

    return cart


def get_cart_items(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart/partials/cart-item-list.html', context)


def cart_view(request):
    # Get the cart instance
    cart = get_cart(request)

    # Get the cart items
    cart_items = cart.items.all()
    total_price = cart.total_price
    subtotal = cart.subtotal
    tax = cart.tax_amount
    discount = cart.display_discount

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'subtotal': subtotal,
        'tax': tax,
        'discount': discount,
    }

    return render(request, 'cart/detail.html', context)


def add_to_cart(request, product_slug):
    # Get or create the cart
    cart = get_cart(request)

    # Get the product instance
    product = get_object_or_404(Product, slug=product_slug)

    # Get or create a cart item for the product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Extract the quantity from the request
    quantity = int(request.POST.get('quantity', 1))

    if created:
        cart_item.quantity = quantity
        messages.success(request, f'{product.name} has been added to your cart')
    else:
        cart_item.quantity += quantity
        if cart_item.quantity <= product.quantity:
            messages.success(request, f'{product.name} quantity has been updated in your cart.')
        else:
            cart_item.quantity -= quantity  # Rollback the quantity increment
            messages.error(request, f'Sorry we only have {product.quantity} units of {product.name} in stock')

    cart_item.save()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'update-cart'
    return response


def increase_item_quantity(request, product_slug):
    # Get the cart
    cart = get_cart(request)

    # Get the product instance
    product = get_object_or_404(Product, slug=product_slug)

    # Get the cart item for the product
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Check if the desired increase exceeds the available stock
    if cart_item.quantity + 1 > product.quantity:
        messages.error(request, f"Quantity of {product.name} cannot exceed available stock.")
    else:
        # Increase quantity
        cart_item.quantity += 1
        cart_item.save()

    # Create an HTTP response with a status of 204 (success) and set an update-cart trigger
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'update-cart'
    return response


def decrease_item_quantity(request, product_slug):
    # Get the cart
    cart = get_cart(request)

    # Get the product instance
    product = get_object_or_404(Product, slug=product_slug)

    # Get the cart item for the product
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Decrease quantity if greater than 2
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.error(request, f'Quantity of {product.name} cannot be less than 1.')

    # Create an HTTP response with a status of 204 (success) and set an update-cart trigger
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'update-cart'
    return response


def remove_cart_item(request, product_slug):
    # Get the cart
    cart = get_cart(request)

    # Get the product_instance
    product = get_object_or_404(Product, slug=product_slug)

    # Get the  cart item for the product
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Remove the cart item from the cart
    cart_item.delete()

    # Create an HTTP response with a status of 204 (success) and set an update-cart trigger
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'update-cart'
    return response


def update_cart_summary(request):
    # Get the cart
    cart = get_cart(request)

    # Get the subtotal, price and total price based on the updated cart item
    subtotal = cart.subtotal
    tax = cart.tax_amount
    total_price = cart.total_price
    discount = cart.display_discount

    context = {
        'subtotal': subtotal,
        'tax': tax,
        'total_price': total_price,
        'discount': discount
    }
    return render(request, 'cart/partials/cart-summary.html', context)


def hx_cart_button(request):
    return render(request, 'navigation/partials/cart-button.html')


def hx_empty_cart(request):
    return render(request, 'cart/partials/empty-cart.html')
