from django.contrib import admin
from .models import Customer, Reservation, Order, Inventory, Payment, Feedback, Staff, SickReport, ShiftChangeRequest, ShiftSwapRequest
 

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
# Register your models here.
