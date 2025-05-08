from django.shortcuts import render, redirect
from core.controllers.reservation_controller import create_reservation, get_reservation_by_id
from core.models import Customer

def reservation_form(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        num_guests = request.POST.get('num_guests')
        table_number = request.POST.get('table_number')

        customer = Customer.objects.get(id=customer_id)
        create_reservation(customer, date, time, num_guests, table_number)
        return redirect('reservation_success')

    return render(request, 'reservation_form.html')


def reservation_success(request):
    return render(request, 'reservation_success.html')

from core.controllers.order_controller import create_order
from django.shortcuts import render, redirect
from core.models import Customer

def order_form(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        total_price = request.POST.get('total_price')
        status = request.POST.get('status')

        try:
            customer = Customer.objects.get(id=customer_id)
            create_order(customer, total_price, status)
            return redirect('order_success')
        except Customer.DoesNotExist:
            return render(request, 'order_form.html', {'error': 'Customer not found'})

    return render(request, 'order_form.html')

def order_success(request):
    return render(request, 'order_success.html')

from django.shortcuts import render, redirect
from core.models import Order
from core.controllers.payment_controller import create_payment

def payment_form(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        method = request.POST.get('method')

        order = Order.objects.get(id=order_id)
        create_payment(order, order.total_price, method)
        return redirect('payment_success', order_id=order.id)

    orders = Order.objects.all()
    return render(request, 'payment_form.html', {'orders': orders})

def payment_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'payment_success.html', {'amount': order.total_price})

from core.models import Customer
from core.controllers.feedback_controller import submit_feedback
from django.shortcuts import render, redirect

def feedback_form(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        message = request.POST.get('message')
        rating = int(request.POST.get('rating'))

        customer = Customer.objects.get(id=customer_id)
        submit_feedback(customer, message, rating)

        return redirect('feedback_success')

    return render(request, 'feedback_form.html')

def feedback_success(request):
    return render(request, 'feedback_success.html')

from django.shortcuts import render, redirect
from core.controllers.staff_controller import (
    request_shift_change,
    report_sick,
    initiate_shift_swap,
)

def staff_portal(request):
    if request.method == 'POST':
        Request_Type = request.POST.get('Request_Type')
        staff_id = int(request.POST.get('staff_id'))
        manager_id = request.POST.get('manager_id')  # optional
        details = request.POST.get('details')  # shift time, reason, conflict, etc.

        if Request_Type == 'report_sick':
            report_sick(staff_id)
        elif Request_Type == 'request_shift':
            request_shift_change(staff_id, details)
        elif Request_Type == 'initiate_swap':
            target_id = int(request.POST.get('target_staff_id'))
            initiate_shift_swap(staff_id, target_id)

        return redirect('staff_success')

    return render(request, 'staff_portal.html')

def staff_success(request):
    return render(request, 'staff_success.html')

from django.shortcuts import render, redirect
from core.controllers.inventory_controller import (
    get_all_inventory,
    update_inventory_quantity,
    remove_discontinued_item,
    monitor_reorder_levels
)

def inventory_portal(request):
    context = {
        'inventory_items': get_all_inventory(),
        'low_stock_items': monitor_reorder_levels()
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')

        if action == 'update':
            new_quantity = int(request.POST.get('new_quantity'))
            update_inventory_quantity(item_id, new_quantity)

        elif action == 'remove':
            remove_discontinued_item(item_id)

        return redirect('inventory_success')

    return render(request, 'inventory_portal.html', context)

def inventory_success(request):
    return render(request, 'inventory_success.html')