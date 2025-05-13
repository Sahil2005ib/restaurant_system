from django import forms
from core.models import MenuItem

class OrderItemForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)