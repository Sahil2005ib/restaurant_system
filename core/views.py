from django.shortcuts import render, redirect
from core.controllers.reservation_controller import create_reservation
from core.services.table_availability import get_available_tables
from core.models import Customer, Table, Reservation
from datetime import datetime, time, timedelta

def generate_time_slots(start="12:00", end="22:00", interval_minutes=30):
    slots = []
    current = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    while current < end_time:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=interval_minutes)
    return slots

def reservation_form(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        date = request.POST.get('date')
        time_str = request.POST.get('time')
        num_guests = request.POST.get('num_guests')
        table_obj = Table.objects.get(id=int(request.POST.get('table_number')))

        print(f"Submitted date: {date}, time: {time_str}")

        hours, minutes = map(int, time_str.split(':'))
        selected_time = time(hours, minutes)

        customer = Customer.objects.get(id=customer_id)
        reservation = create_reservation(customer, date, selected_time, num_guests, table_obj)

        # Redirect to confirmation page, passing reservation ID
        return redirect('reservation_success', reservation_id=reservation.id)
    
    # GET
    date_str = request.GET.get('date', datetime.today().date().isoformat())
    time_str = request.GET.get('time', '12:00')

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        selected_date = datetime.today().date()

    try:
         hours, minutes = map(int, time_str.split(':'))
         selected_time = time(hours, minutes)
    except ValueError:
        selected_time = time(12, 0)

    available_tables = get_available_tables(selected_date, selected_time)
    time_slots = generate_time_slots()

    return render(request, 'reservation_form.html', {
        'available_tables': available_tables,
        'date': selected_date,
        'time': time_str,
        'time_slots': time_slots,
    })

def reservation_success(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'reservation_success.html', {
        'reservation': reservation
    })

from core.models import MenuItem, OrderItem, Customer, Order
from core.services.order_notifier import notify_kitchen_of_order
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

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
            return HttpResponseRedirect(f"/payment?order_id={order.id}")
        
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
from core.services.payment_gateway import update_order_payment_status
from core.controllers.payment_controller import get_payments_for_order

def payment_form(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        method = request.POST.get('method')

        order = Order.objects.get(id=order_id)
     
        payment = create_payment(order, order.total_price, method)

        if not payment:
            return render(request, 'payment_form.html', {
                'orders': Order.objects.all(),
                'error': f"Payment failed for Order #{order.id}. Please try again."
            })
        
        update_order_payment_status(order)
        return redirect('payment_success', order_id=order.id)
    
    preselected_order_id = request.GET.get('order_id')
    orders = Order.objects.all()
    return render(request, 'payment_form.html', {
        'orders': orders,
        'preselected_order_id': preselected_order_id,
    })

def payment_success(request, order_id):
    order = Order.objects.get(id=order_id)
    payments = get_payments_for_order(order_id)

    return render(request, 'payment_success.html', {
        'order': order,
        'payments': payments
    })

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
from core.controllers.report_controller import create_report, get_reports_by_type, filter_reports_by_date
from core.models import Staff
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def report_portal(request):
    message = ""
    reports = []
    start_date = end_date = None

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        report_type = request.POST.get('report_type')
        filters = request.POST.get('filters')
        file_link = request.POST.get('file_link', "")

        # Optional: Filter range
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            manager = Staff.objects.get(id=staff_id, role='manager', is_active=True)

            if start_date and end_date:
                reports = filter_reports_by_date(start_date, end_date)
                if not reports.exists():
                    message = "⚠️ No data found in selected range. Try changing the dates."
            else:
                create_report(manager, report_type, filters, file_link)
                return redirect('report_success')

        except ObjectDoesNotExist:
            message = "⚠️ Selected manager does not exist."
        except Exception as e:
            message = str(e)

    managers = Staff.objects.filter(role='manager', is_active=True)
    return render(request, 'report_portal.html', {
        'managers': managers,
        'reports': reports,
        'message': message,
        'start_date': start_date,
        'end_date': end_date,
    })

def report_success(request):
    return render(request, 'report_success.html')