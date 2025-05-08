from core.models import Feedback
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def submit_feedback(customer, message, rating):
    """Create a new feedback entry and alert manager if urgent."""
    is_urgent = rating <= 2
    feedback = Feedback.objects.create(
        customer=customer,
        comment=message,
        rating=rating,
        is_urgent=is_urgent,
        submitted_at=timezone.now()
    )

    if rating <= 2:
        print(f"⚠️ Urgent feedback submitted by {customer.name}: {message}")

    return feedback

def get_all_feedback():
    """Retrieve all feedback entries, most recent first."""
    return Feedback.objects.all().order_by('-submitted_at')

def get_feedback_by_id(feedback_id):
    """Retrieve a single feedback entry by its ID."""
    try:
        return Feedback.objects.get(id=feedback_id)
    except ObjectDoesNotExist:
        return None

def delete_feedback(feedback_id):
    """Delete a specific feedback entry."""
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.delete()
        return True
    except ObjectDoesNotExist:
        return False

def get_feedback_summary():
    """Return a quick summary such as average rating."""
    all_feedback = Feedback.objects.all()
    if not all_feedback.exists():
        return {
            'total': 0,
            'average_rating': 0,
        }
    total = all_feedback.count()
    avg_rating = round(sum(f.rating for f in all_feedback) / total, 2)
    return {
        'total': total,
        'average_rating': avg_rating,
    }

def is_urgent_feedback(message, rating):
    """Define criteria for urgent feedback."""
    urgent_keywords = ['unsafe', 'allergic', 'complaint', 'rude', 'injury']
    contains_urgent_word = any(word in message.lower() for word in urgent_keywords)
    return contains_urgent_word or rating <= 2

def alert_manager(feedback):
    """Simulate alert to manager for urgent feedback."""
    print(f"[ALERT] Urgent feedback from {feedback.customer.name}: {feedback.message}")