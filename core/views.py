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

from core.models import MenuItem, OrderItem, Customer, Order
from core.services.order_notifier import notify_kitchen_of_order
from django.shortcuts import render, redirect

def order_form(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        menu_item_ids = request.POST.getlist('menu_item')
        quantities = request.POST.getlist('quantity')

        try:
            customer = Customer.objects.get(id=customer_id)
            order = Order.objects.create(customer=customer, status='new', total_price=0)

            total_price = 0
            for item_id, qty in zip(menu_item_ids, quantities):
                item = MenuItem.objects.get(id=item_id)
                quantity = int(qty)
                OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)
                total_price += item.price * quantity

            order.total_price = total_price
            order.save()

            notify_kitchen_of_order(order)
            return redirect('order_success')
        except Exception as e:
            return render(request, 'order_form.html', {
                'error': str(e),
                'menu_items': MenuItem.objects.all()
            })

    return render(request, 'order_form.html', {
        'menu_items': MenuItem.objects.all()
    })

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

from django.shortcuts import render, redirect
from core.controllers.report_controller import create_report, get_reports_by_type
from core.models import Staff
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def report_portal(request):
    message = ""
    reports = []

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        report_type = request.POST.get('report_type')
        filters = request.POST.get('filters')
        file_link = request.POST.get('file_link', "")

        try:
            manager = Staff.objects.get(id=staff_id, role='manager', is_active=True)
            create_report(manager, report_type, filters, file_link)
            return redirect('report_success')
        except ObjectDoesNotExist:
            message = "Selected manager does not exist."
        except Exception as e:
            message = str(e)

    # Load manager dropdown list
    managers = Staff.objects.filter(role='manager', is_active=True)
    reports = get_reports_by_type('sales')

    return render(request, 'report_portal.html', {
        'managers': managers,
        'reports': reports,
        'message': message,
        'now': timezone.now().date(),
    })

def report_success(request):
    return render(request, 'report_success.html')