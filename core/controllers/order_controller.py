from core.models import Order, Customer
from django.core.exceptions import ObjectDoesNotExist
from core.services.order_notifier import notify_kitchen_of_order

from core.models import Order

def create_order(customer, total_price, status):
    """Creates a new order."""
    order = Order.objects.create(
        customer=customer,
        total_price=total_price,
        status=status
    )
    return order

def get_customer_orders(customer_id):
    """Return all orders placed by a customer."""
    return Order.objects.filter(customer_id=customer_id).order_by('-date')

def update_order_status(order_id, new_status):
    """Update the status of an existing order."""
    try:
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        return order
    except ObjectDoesNotExist:
        return None

def mark_order_paid(order_id):
    """Set the is_paid flag of an order to True."""
    try:
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()
        return order
    except ObjectDoesNotExist:
        return None

def delete_order(order_id):
    """Delete an order from the database."""
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return True
    except ObjectDoesNotExist:
        return False
    

def create_order(customer, total_price, status):
    """Creates a new order and notifies kitchen."""
    order = Order.objects.create(
        customer=customer,
        total_price=total_price,
        status=status
    )

    notify_kitchen_of_order(order)  # ✅ Now it's using a real order instance
    print(f"🧾 New order received from: {order.customer.name}")
    return order