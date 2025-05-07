from django.contrib import admin
from .models import Customer, Reservation, Order, Inventory, Payment, Feedback, Staff

admin.site.register(Customer)
admin.site.register(Reservation)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(Staff)
# Register your models here.
