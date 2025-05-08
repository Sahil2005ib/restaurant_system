from core.models import Staff, SickReport, ShiftChangeRequest, ShiftSwapRequest
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Example placeholder for schedule-related model (if used later)
# from core.models import Schedule


def request_shift_change(staff_id, requested_shift):
    try:
        staff = Staff.objects.get(id=staff_id)
        ShiftChangeRequest.objects.create(
            staff=staff,
            requested_shift=requested_shift,
            status='pending'
        )
        return True
    except Staff.DoesNotExist:
        return False


def initiate_shift_swap(staff_id, target_staff_id):
    try:
        requester = Staff.objects.get(id=staff_id)
        target = Staff.objects.get(id=target_staff_id)
        ShiftSwapRequest.objects.create(
            requester=requester,
            target=target,
            status='pending'
        )
        return True
    except Staff.DoesNotExist:
        return False


def report_sick(staff_id, date=None):
    """Save a sick report to the database."""
    try:
        staff = Staff.objects.get(id=staff_id)
        date = date or timezone.now().date()
        
        # Save to DB
        SickReport.objects.create(
            staff=staff,
            sick_date=date,
            status='pending'  # default status
        )
        print(f"{staff.name} reported sick on {date}.")
        return True
    except ObjectDoesNotExist:
        return False


