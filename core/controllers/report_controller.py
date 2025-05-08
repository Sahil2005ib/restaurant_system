from core.models import Report, Staff
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def create_report(staff, report_type, filters, file_link=None):
    """Create a report (only if staff is a manager)."""
    if staff.role != 'manager':
        raise PermissionError("Only managers can create reports.")
    
    report = Report.objects.create(
        created_by=staff,
        report_type=report_type,
        filters=filters,
        created_at=timezone.now(),
        file_link=file_link or ""
    )
    return report

def get_reports_by_type(report_type):
    """Get all reports of a specific type."""
    return Report.objects.filter(report_type=report_type).order_by('-created_at')

def get_report_by_id(report_id):
    """Fetch a report by its ID."""
    try:
        return Report.objects.get(id=report_id)
    except ObjectDoesNotExist:
        return None

def filter_reports_by_date(start_date, end_date):
    """Filter reports created between two dates."""
    return Report.objects.filter(created_at__range=[start_date, end_date]).order_by('-created_at')