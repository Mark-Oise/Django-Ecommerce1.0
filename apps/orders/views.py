from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import OrderCreationForm
from .models import OrderItem, Order
from .tasks import order_created
from apps.cart.views import get_cart
import weasyprint


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
    cart_items = cart.items.all() if request.method == 'GET' else []  # Initialize cart_items conditionally

    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()

            # Create order items based on cart items
            OrderItem.objects.create([
                OrderItem(order=order, product=item.product, price=item.price, quantity=item.quantity)
                for item in cart_items
            ])
            cart.items.all().delete()

            # Trigger the order_created task asynchronously
            order_created.delay(order.id)

            # Set the order in the session
            request.session['order_id'] = order.id

            # Redirect to the payment:process URL
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreationForm()
        cart_items = cart.items.all()  # Populate cart_items with the actual data

    return render(request, 'orders/create.html', {'form': form, 'cart_items': cart_items})


def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-disposition'] = f'filename=order_{order.order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response
