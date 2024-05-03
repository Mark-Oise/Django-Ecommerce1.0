from django.urls import path
from .views import process_payment, payment_completed, payment_cancelled
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('process/', process_payment, name='process'),
    path('completed/', payment_completed, name='completed'),
    path('canceled/', payment_cancelled, name='canceled'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]
