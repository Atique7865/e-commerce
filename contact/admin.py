"""
contact/admin.py
Admin configuration for contact-form messages.
"""
from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('subject', 'name', 'email', 'phone', 'is_read', 'created_at')
    list_filter   = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)

    def has_add_permission(self, request):
        # Messages come from the public form only — disallow manual creation
        return False
