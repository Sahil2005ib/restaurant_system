from core.models import Payment
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from core.models import SalesReport, Staff

def create_payment(order, amount, method):
    """Create a payment for a given order."""
    already_paid = get_total_paid(order.id)

    if amount + already_paid > order.total_price:
        print(f"❌ Payment failed: trying to overpay Order #{order.id}")
        return None  # Simulate failure

    payment = Payment.objects.create(
        order=order,
        amount=order.total_price,
        method=method,
        timestamp=timezone.now()
    )

    print(f"✅ Payment recorded for Order #{order.id}: £{amount} via {method}")
    
    # Mark as paid if fully covered
    total_paid = get_total_paid(order.id)
    if total_paid >= order.total_price:
        order.is_paid = True
        if order.status != 'split_pending': 
            order.status = 'paid' 
        order.save()
        print(f"✅ Order #{order.id} marked as PAID.")

    if not SalesReport.objects.filter(order=order).exists():
        manager = getattr(order, 'staff', None)  # or assign manually
        SalesReport.objects.create(
            order=order,
            amount=payment.amount,
            manager=manager,
            date=timezone.now().date()
        )
        print(f"📊 SalesReport created for Order #{order.id}")

    return payment

def get_payments_for_order(order_id):
    """Retrieve all payments made for a specific order."""
    return Payment.objects.filter(order__id=order_id)

def get_total_paid(order_id):
    """Calculate the total amount paid for an order."""
    return sum(p.amount for p in Payment.objects.filter(order__id=order_id))

# core/controllers/payment_controller.py

def handle_split_bill(order):
    """Mark the order as split and log it for waitstaff."""
    order.status = 'split_pending'
    order.is_split = True  # ✅ flag for waitstaff to check on dashboard
    order.save()
    print(f"🔔 Order #{order.id} marked as split bill (awaiting full payment or confirmation).")