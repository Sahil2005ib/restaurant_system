from django.contrib import admin
from .models import Customer, Reservation, Order, Inventory, Payment, Feedback, Staff, SickReport, ShiftChangeRequest, ShiftSwapRequest, Report, MenuItem, OrderItem, UserProfile
 

admin.site.register(Customer)
admin.site.register(Reservation)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(Staff)
admin.site.register(SickReport)
admin.site.register(ShiftChangeRequest)
admin.site.register(ShiftSwapRequest)
admin.site.register(Report)
admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(UserProfile)

# Register your models here.
