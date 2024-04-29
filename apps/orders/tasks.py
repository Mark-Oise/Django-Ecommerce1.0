from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = get_object_or_404(Order, id=order_id)
    subject = f'order {order.order_id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.order_id}.'
    mail_sent = send_mail(
        subject,
        message,
        'admin@website.com',
        [order.email]
    )
    return mail_sent
