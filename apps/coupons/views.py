from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .forms import ApplyCouponForm
from .models import Coupon
from apps.cart.views import get_cart


# Create your views here.

def apply_coupon(request):
    """
    View function to handle the coupon application process.

    This view retrieves the current cart, validates the coupon form,
    and applies the coupon to the cart if it is valid.

    """
    cart = get_cart(request)
    now = timezone.now()
    coupon_code = request.POST.get('code')

    if request.method == 'POST':
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
        else:
            if cart.coupon and cart.coupon.code == coupon.code:
                messages.error(request, 'The coupon is already applied to your cart.')
            elif coupon.active:
                cart.coupon = coupon
                cart.save()
                messages.success(request, 'Coupon applied successfully.')
            else:
                messages.error(request, 'The coupon is no longer valid.')

    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'update-cart'
    return response


def remove_coupon(request):
    """
    View function to handle the coupon removal process.

    This view retrieves the current cart and removes the applied
    coupon if one exists.

    """
    cart = get_cart(request)  # Get the current cart

    if cart.coupon:
        coupon = cart.coupon  # Get the applied coupon
        cart.coupon = None  # Remove the coupon from the cart
        cart.save()  # Save the cart without the coupon
        messages.success(request, f'Coupon "{coupon.code}" has been removed.')  # Display a success message
    else:
        messages.error(request, 'There is no coupon applied to your cart.')  # Display an error message

    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'update-cart'
    return response
