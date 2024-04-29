from django.contrib.auth import get_user_model
from django.db import models
from apps.products.models import Product
from apps.coupons.models import Coupon
from django.contrib.sessions.models import Session
from decimal import Decimal
from django.conf import settings


class Cart(models.Model):
    """
    Represents a shopping cart associated with a session.
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the cart.
        """
        return f'Cart {self.id}'

    @property
    def total_items(self):
        """
        Calculates and returns the total number of items in the cart.
        """
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """
        Calculates and returns the subtotal price of all items in the cart.
        """
        return sum(item.total_price for item in self.items.all())

    @property
    def tax_amount(self):
        """
        Calculates and returns the tax amount based on the subtotal and tax rate.
        """
        tax_percentage = Decimal('0.15')
        tax_amount = self.subtotal * tax_percentage
        return tax_amount

    @property
    def total_price(self):
        """
        Calculates and returns the total price including tax and discounts.
        """
        subtotal = self.subtotal
        if self.coupon:
            if self.coupon.discount_type == 'Percentage':
                discount = subtotal * (self.coupon.value / Decimal('100'))
            else:
                discount = self.coupon.value
            subtotal -= discount

        tax_amount = subtotal * Decimal('0.15')
        total_price = subtotal + tax_amount

        return total_price

    def display_discount(self):
        """
        Returns a string representing the discount value and type.
        """
        if self.coupon and self.coupon.discount_type:
            discount_value = self.coupon.value

            if self.coupon.discount_type == 'Percentage':
                discount_display = f"-{discount_value:.0f}% off"
            else:
                discount_display = f"-${int(discount_value)}"

            return discount_display

        return ""

    def count_items(self):
        """
        Counts and returns the total number of items in the cart.
        """
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Represents an item in a shopping cart.
    """

    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Returns a string representation of the cart item.
        """
        return f'{self.product.name} {self.quantity}'

    @property
    def price(self):
        """
        Returns the price of the product associated with the cart item.
        """
        return self.product.price

    @property
    def total_price(self):
        """
        Calculates and returns the total price of the cart item (price * quantity).
        """
        return self.price * self.quantity
