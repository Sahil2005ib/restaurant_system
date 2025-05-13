from core.models import Order
from core.controllers.payment_controller import get_total_paid

def update_order_payment_status(order):
    """
    Check if an order has been fully paid and update its status accordingly.
    """
    total_paid = get_total_paid(order.id)

    if total_paid >= order.total_price:
        order.is_paid = True
        order.save()
        print(f"✅ Order #{order.id} marked as PAID.")
    else:
        print(f"💰 Partial payment for Order #{order.id}: £{total_paid:.2f} / £{order.total_price:.2f}")