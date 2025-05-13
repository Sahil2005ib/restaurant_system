from core.models import Reservation, Table

def get_available_tables(date, time_slot):
    print(f"Looking for tables on date: {date}, time: {time_slot}")
    
    # Get all reservations for this date and time
    reservations = Reservation.objects.filter(date=date, time=time_slot)
    print(f"Found {reservations.count()} reservation(s) for this time slot")
    
    # Get reserved table IDs from these reservations
    reserved_table_ids = reservations.values_list('table_number__id', flat=True)
    print(f"Reserved table IDs: {list(reserved_table_ids)}")
    
    # Exclude these reserved tables from all tables
    available = Table.objects.exclude(id__in=reserved_table_ids)
    print(f"Available tables: {[t.number for t in available]}")
    
    return available