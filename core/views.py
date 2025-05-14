from django.shortcuts import render, redirect
from core.controllers.reservation_controller import create_reservation
from core.services.table_availability import get_available_tables
from core.models import Customer, Table, Reservation
from datetime import datetime, time, timedelta
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .models import MenuItem
from django.contrib.auth import logout
from core.controllers.feedback_controller import get_all_feedback
from core.models import StaffRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SalesReport
from core.models import Inventory, StaffRequest, Report, RestockRequest, ShiftChangeRequest, ShiftSwapRequest, SickReport
from django.utils import timezone


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.userprofile.role
            if role == 'customer':
                return redirect('customer_dashboard')
            elif role == 'waitstaff':
                return redirect('staff_dashboard')
            elif role == 'kitchen':
                return redirect('kitchen_dashboard')
            elif role == 'inventory':
                return redirect('inventory_dashboard')
            elif role == 'manager':
                return redirect('manager_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def request_restock(request):
    items = Inventory.objects.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        qty = request.POST.get('quantity')

        item = Inventory.objects.get(id=item_id)
        RestockRequest.objects.create(
            item=item,
            quantity_requested=qty,
            requested_by=request.user.staff  # assuming request.user has a related Staff object
        )
        return redirect('restock_request_success')

    return render(request, 'request_restock.html', {
        'items': items,
    })

@login_required
def restock_approval_portal(request):
    requests = RestockRequest.objects.filter(is_approved=False)

    if request.method == 'POST':
        approved_ids = request.POST.getlist('approve')
        for req_id in approved_ids:
            restock = RestockRequest.objects.get(id=req_id)
            restock.is_approved = True
            restock.approved_by = request.user.staff
            restock.approved_at = timezone.now()
            restock.save()

            # Optional: update inventory quantity
            restock.item.quantity += restock.quantity_requested
            restock.item.restock_approved = True
            restock.item.save()

        return redirect('restock_approval_portal')

    return render(request, 'restock_approval_portal.html', {
        'requests': requests
    })

@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

@login_required
def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'menu_list.html', {'menu_items': items})

@login_required
def manager_dashboard(request):
    urgent_feedback = get_all_feedback().filter(is_urgent=True).order_by('-submitted_at')
    shift_change_requests = ShiftChangeRequest.objects.filter(status='pending')
    shift_swap_requests = ShiftSwapRequest.objects.filter(status='pending')
    sick_reports = SickReport.objects.filter(status='pending')
    recent_reports = Report.objects.order_by('-created_at')[:5]
    low_stock_items = Inventory.objects.filter(quantity__lt=10)
    pending_restock_requests = RestockRequest.objects.filter(is_approved=False).order_by('-requested_at')

    return render(request, 'manager_dashboard.html', {
        'urgent_feedback': urgent_feedback,
        'shift_change_requests': shift_change_requests,
        'shift_swap_requests': shift_swap_requests,
        'sick_reports': sick_reports,
        'recent_reports': recent_reports,
        'low_stock_items': low_stock_items,
        'pending_restock_requests': pending_restock_requests,
    })
@login_required
def inventory_approval_portal(request):
    pending_requests = RestockRequest.objects.filter(is_approved=False)

    if request.method == 'POST':
        approved_ids = request.POST.getlist('approve')
        for req_id in approved_ids:
            restock = RestockRequest.objects.get(id=req_id)
            restock.is_approved = True
            restock.approved_at = timezone.now()
            restock.item.quantity += restock.quantity_requested
            restock.item.save()
            restock.save()

        return redirect('inventory_approval_portal')

    return render(request, 'inventory_approval_portal.html', {
        'pending_requests': pending_requests
    })

# views.py
@login_required
def approve_shift_change(request, request_id):
    req = get_object_or_404(ShiftChangeRequest, id=request_id)
    req.status = 'approved'
    req.save()
    return redirect('manager_dashboard')

@login_required
def reject_shift_change(request, request_id):
    req = get_object_or_404(ShiftChangeRequest, id=request_id)
    req.status = 'rejected'
    req.save()
    return redirect('manager_dashboard')

@login_required
def approve_shift_swap(request, request_id):
    req = get_object_or_404(ShiftSwapRequest, id=request_id)
    req.status = 'approved'
    req.save()
    return redirect('manager_dashboard')

@login_required
def reject_shift_swap(request, request_id):
    req = get_object_or_404(ShiftSwapRequest, id=request_id)
    req.status = 'rejected'
    req.save()
    return redirect('manager_dashboard')

@login_required
def approve_sick_report(request, report_id):
    report = get_object_or_404(SickReport, id=report_id)
    report.status = 'approved'
    report.save()
    return redirect('manager_dashboard')

@login_required
def reject_sick_report(request, report_id):
    report = get_object_or_404(SickReport, id=report_id)
    report.status = 'rejected'
    report.save()
    return redirect('manager_dashboard')


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
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        num_guests = request.POST.get('num_guests')
        table_obj = Table.objects.get(id=int(request.POST.get('table_number')))
        
        print(f"Submitted date: {date_str}, time: {time_str}")
        
        # Parse time string into time object
        hours, minutes = map(int, time_str.split(':'))
        selected_time = time(hours, minutes)
        
        customer = Customer.objects.get(id=customer_id)
        
        # Pass the time object to create_reservation
        reservation = create_reservation(customer, date_str, selected_time, num_guests, table_obj)
        
        return redirect('reservation_success', reservation_id=reservation.id)
    
    # GET request handling
    date_str = request.GET.get('date', datetime.today().date().isoformat())
    time_str = request.GET.get('time', '12:00')
    
    print(f"GET request - date={date_str}, time={time_str}")
    
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        selected_date = datetime.today().date()
    
    try:
        hours, minutes = map(int, time_str.split(':'))
        selected_time = time(hours, minutes)
    except ValueError:
        selected_time = time(12, 0)
    
    # Check availability for the selected date and time, not the default
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
from django.contrib.auth.decorators import login_required
from core.models import Inventory, RestockRequest, Staff
from django.utils import timezone

@login_required
def inventory_portal(request):
    inventory_items = Inventory.objects.all()
    low_stock_items = Inventory.objects.filter(quantity__lt=10)

    if request.method == 'POST':
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')

        try:
            staff_user = Staff.objects.get(name=request.user.username)
        except Staff.DoesNotExist:
            messages.error(request, "⚠️ Your staff profile could not be found.")
            return redirect('inventory_portal')

        if action == 'update':
            new_qty = int(request.POST.get('new_quantity'))
            item = Inventory.objects.get(id=item_id)
            item.quantity = new_qty
            item.save()

        elif action == 'remove':
            Inventory.objects.filter(id=item_id).delete()

        elif action == 'request_restock':
            item = Inventory.objects.get(id=item_id)
            qty = int(request.POST.get('quantity'))

            staff_user = Staff.objects.get(email=request.user.email)
            RestockRequest.objects.create(
                item=item,
                quantity_requested=qty,
                requested_by=staff_user,
                is_approved=False,
                requested_at=timezone.now()
            )

        return redirect('inventory_portal')

    return render(request, 'inventory_portal.html', {
        'inventory_items': inventory_items,
        'low_stock_items': low_stock_items
    })

def inventory_success(request):
    return render(request, 'inventory_success.html')

from core.models import Staff, Feedback, SalesReport, Inventory
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date

@login_required
def report_portal(request):
    message = ""
    reports = []
    report_type = None
    start_date = end_date = None

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        report_type = request.POST.get('report_type')

        # Parse date range
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_dt = parse_date(start_date) if start_date else None
        end_dt = parse_date(end_date) if end_date else None

        try:
            manager = Staff.objects.get(id=staff_id, role='manager', is_active=True)

            # Load appropriate reports
            if report_type == 'feedback':
                reports = Feedback.objects.all()
                if start_dt and end_dt:
                    reports = reports.filter(submitted_at__date__range=(start_dt, end_dt))
                if filters:
                    reports = reports.filter(comment__icontains=filters)

            elif report_type == 'sales':
                reports = SalesReport.objects.all()
                if start_dt and end_dt:
                    reports = reports.filter(date__range=(start_dt, end_dt))
                # Optional: also filter by manager
                reports = reports.filter(manager=manager)

            elif report_type == 'inventory':
                reports = Inventory.objects.all()
                if start_dt and end_dt:
                    reports = reports.filter(last_updated__date__range=(start_dt, end_dt))
                if filters:
                    reports = reports.filter(name__icontains=filters)

            else:
                message = "⚠️ Invalid report type selected."

            if not reports.exists():
                message = "⚠️ No data found in selected range. Try changing the dates."

        except ObjectDoesNotExist:
            message = "⚠️ Selected manager does not exist."
        except Exception as e:
            message = str(e)

    managers = Staff.objects.filter(role='manager', is_active=True)
    return render(request, 'report_portal.html', {
        'managers': managers,
        'reports': reports,
        'report_type': report_type,
        'message': message,
        'start_date': start_date,
        'end_date': end_date,
    })

def report_success(request):
    return render(request, 'report_success.html')