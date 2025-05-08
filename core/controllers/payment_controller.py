from core.models import Payment
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def create_payment(order, amount, method):
    """Create a payment for a given order."""
    payment = Payment.objects.create(
        order=order,
        amount=order.total_price,
        method=method,
        timestamp=timezone.now()
    )
    return payment

def get_payments_for_order(order_id):
    """Retrieve all payments made for a specific order."""
    return Payment.objects.filter(order__id=order_id)

def get_total_paid(order_id):
    """Calculate the total amount paid for an order."""
    return sum(p.amount for p in Payment.objects.filter(order__id=order_id))