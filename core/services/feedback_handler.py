from core.models import Feedback, Staff
from django.core.mail import send_mail
from django.utils import timezone

def validate_feedback_input(data):
    """Check for required fields in feedback."""
    required_fields = ['customer', 'comment', 'rating']
    for field in required_fields:
        if not data.get(field):
            return False
    return True

def handle_feedback_submission(data):
    """Process feedback and alert manager if urgent."""
    if not validate_feedback_input(data):
        raise ValueError("Missing required feedback fields.")
    
    feedback = Feedback.objects.create(
        customer=data['customer'],
        comment=data['comment'],
        rating=data['rating'],
        is_urgent=data.get('is_urgent', False),
        submitted_at=timezone.now()
    )

    if feedback.is_urgent:
        notify_managers_of_urgent_feedback(feedback)
    
    return feedback

def notify_managers_of_urgent_feedback(feedback):
    """Notify all active managers about urgent feedback."""
    managers = Staff.objects.filter(role='manager', is_active=True)
    subject = "Urgent Feedback Received"
    message = f"Urgent feedback from Customer ID {feedback.customer.id}:\n\n{feedback.comment}"

    for manager in managers:
        send_mail(
            subject,
            message,
            'noreply@restaurant-system.com',
            [manager.email],
            fail_silently=True,
        )