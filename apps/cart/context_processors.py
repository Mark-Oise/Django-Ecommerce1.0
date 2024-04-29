from .views import get_cart


def cart_context(request):
    # Retrieve the cart using the get_cart utility function
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
        'cart': cart,
        'discount': discount
    }

    return context
