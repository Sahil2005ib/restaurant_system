from core.models import Inventory
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def get_all_inventory():
    """Return all inventory items ordered by last updated."""
    return Inventory.objects.all().order_by('-last_updated')


def update_inventory_quantity(item_id, new_quantity):
    """Update the quantity of a specific inventory item."""
    try:
        item = Inventory.objects.get(id=item_id)
        item.quantity += new_quantity
        item.last_updated = timezone.now()
        item.save()
        return item
    except ObjectDoesNotExist:
        return None


def monitor_reorder_levels():
    """Return items that are below their reorder threshold."""
    return Inventory.objects.filter(quantity__lt=10)  # example threshold logic


def remove_discontinued_item(item_id):
    """Remove an item that is discontinued."""
    try:
        item = Inventory.objects.get(id=item_id)
        item.delete()
        return True
    except ObjectDoesNotExist:
        return False


def choose_alternative_supplier(item_id, new_supplier_name):
    """Update item to reflect a change in supplier."""
    try:
        item = Inventory.objects.get(id=item_id)
        item.supplier = new_supplier_name  # assuming you have a supplier field
        item.last_updated = timezone.now()
        item.save()
        return item
    except ObjectDoesNotExist:
        return None
