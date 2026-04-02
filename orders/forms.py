"""
orders/forms.py
Form for creating/editing an order.
"""
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Client-facing order/booking form."""

    class Meta:
        model = Order
        fields = ('service', 'project_name', 'project_description', 'budget_range', 'deadline')
        widgets = {
            'project_description': forms.Textarea(attrs={'rows': 5}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'deadline': 'Leave blank if flexible.',
        }

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-select and lock the service if passed from the URL
        if service:
            self.fields['service'].initial = service
            self.fields['service'].widget  = forms.HiddenInput()
