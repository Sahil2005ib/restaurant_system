from core.models import Order, Staff
from django.core.mail import send_mail

def notify_kitchen_of_order(order):
    from core.models import Customer  # Safe to place here to avoid circular import
    customer = Customer.objects.get(id=order.customer_id)

    print(f"🍽️ New order received! Notifying kitchen: Order #{order.id} by {customer.name}")

    kitchen_staff = Staff.objects.filter(role='kitchen', is_active=True)

    items = order.orderitem_set.all()
    item_list = ", ".join(f"{item.quantity}x {item.menu_item.name}" for item in items)

    subject = f"🍽️ New Order #{order.id} Received"
    message = f"A new order has been placed by {customer.name}:\n\nItems: {item_list}\nTotal: £{order.total_price}"

    for staff in kitchen_staff:
        if staff.email:
            send_mail(
                subject,
                message,
                'noreply@restaurant-system.com',
                [staff.email],
                fail_silently=True,
            )

def format_order_summary(order):
    """Return a brief summary string of the order (optional helper)."""
    return f"Order #{order.id} | {order.customer.name} | Total: £{order.total_price}"