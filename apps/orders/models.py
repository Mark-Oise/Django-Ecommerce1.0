import uuid
from django.db import models
from django.utils import timezone
from apps.products.models import Product


# Create your models here.


def generate_order_id():
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:6]
    order_id = f'ORD-{timestamp}-{unique_id}'
    return order_id


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('delivering', 'Delivering'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Order: {self.order_id}'

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def total_price(self):
        return self.price * self.quantity
