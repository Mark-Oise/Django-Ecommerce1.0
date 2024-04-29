from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def clear_filters(request):
    # Clear any filter logic here
    # For example, reset any session variables storing filter settings

    # Retrieve all products (or apply any default filtering logic)
    products = Product.objects.all()

    # Render the updated product list
    return render(request, 'store/partials/product-items.html', {'products': products})
