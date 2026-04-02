"""
contact/forms.py
Contact form with basic spam protection via honeypot field.
"""
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Public contact form — saves to DB and sends an email notification."""

    # Hidden honeypot field; bots fill it in, humans don't
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label='')

    class Meta:
        model  = ContactMessage
        fields = ('name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
            'phone':   forms.TextInput(attrs={'placeholder': '+1 (555) 000-0000'}),
        }

    def clean_honeypot(self):
        """Reject submission if the honeypot field was filled."""
        value = self.cleaned_data.get('honeypot', '')
        if value:
            raise forms.ValidationError('Spam detected.')
        return value
