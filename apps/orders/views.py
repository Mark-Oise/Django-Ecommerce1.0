from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import OrderCreationForm
from .models import OrderItem
from .tasks import order_created
from apps.cart.views import get_cart

# Create your views here.


def get_order_items(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    context = {
        'cart_items': cart_items
    }
    return render(request, 'orders/partials/order-item-list.html', context)


def update_order_summary(request):
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
    return render(request, 'orders/partials/order-summary.html', context)


def create_order(request):
    cart = get_cart(request)
    cart_items = []  # Initialize cart_items with an empty list

    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()

            # Create order items based on cart items
            cart_items = cart.items.all()
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.price,
                    quantity=cart_item.quantity
                )
            cart_item.delete()

            # Set the order in the session
            request.session['order_id'] = order.id

            # Trigger the order_created task asynchronously
            order_created.delay(order.id)

            # Redirect to the payment:process URL
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreationForm()
        cart_items = cart.items.all()  # Populate cart_items with the actual data

    return render(request, 'orders/create.html', {'form': form, 'cart_items': cart_items})
