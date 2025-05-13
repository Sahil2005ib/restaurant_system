from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    
class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.PositiveIntegerField()
    table_number = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.name} - {self.date} at {self.time}"
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.id}"
    
class Inventory(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)  # e.g. 'kg', 'litres', 'pcs'
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=50)  # e.g. 'card', 'cash', 'paypal'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of £{self.amount} for Order #{self.order.id}"

class Feedback(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # rating from 1 to 5
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback ({self.rating}/5)"
    
class Staff(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('waitstaff', 'Waitstaff'),
        ('kitchen', 'Kitchen Staff'),
        ('inventory', 'Inventory Staff'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.role})"
    
class SickReport(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_reported = models.DateField(auto_now_add=True)
    sick_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, approved, rejected

    def __str__(self):
        return f"{self.staff.name} reported sick for {self.sick_date}"
    
class ShiftChangeRequest(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    requested_shift = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, approved, rejected
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.name} requests: {self.requested_shift}"

class ShiftSwapRequest(models.Model):
    requester = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='swap_requests')
    target = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='swap_targets')
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, approved

    def __str__(self):
        return f"{self.requester.name} ↔ {self.target.name}"
    
class Report(models.Model):
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('inventory', 'Inventory Report'),
        ('feedback', 'Feedback Report'),
        ('staff', 'Staff Report'),
    ]

    created_by = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'manager'})
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    filters = models.TextField(blank=True)  # JSON or string of selected filters
    created_at = models.DateTimeField(auto_now_add=True)
    file_link = models.URLField(blank=True)  # optional export/download link

    def __str__(self):
        return f"{self.report_type} by {self.created_by} on {self.created_at.date()}"
    