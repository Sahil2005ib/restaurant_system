from core.models import Reservation, Customer
from django.core.exceptions import ObjectDoesNotExist

def create_reservation(customer, date, time, num_guests, table_obj):
    reservation = Reservation.objects.create(
        customer=customer,
        date=date,
        time=time,
        num_guests=num_guests,
        table_number=table_obj
    )
    return reservation  

def get_customer_reservations(customer_id):
    """Returns all reservations for a specific customer."""
    return Reservation.objects.filter(customer_id=customer_id).order_by('-date')

def update_reservation(reservation_id, **kwargs):
    """Updates the details of a reservation."""
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        for key, value in kwargs.items():
            setattr(reservation, key, value)
        reservation.save()
        return reservation
    except ObjectDoesNotExist:
        return None

def cancel_reservation(reservation_id):
    """Deletes a reservation."""
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        return True
    except ObjectDoesNotExist:
        return False
    
def get_reservation_by_id(reservation_id):
    """Fetch a reservation by its ID."""
    try:
        return Reservation.objects.get(id=reservation_id)
    except ObjectDoesNotExist:
        return None