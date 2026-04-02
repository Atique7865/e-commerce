"""
orders/admin.py
Admin panel for managing client orders.
"""
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ('id', 'user', 'service', 'status', 'budget_range', 'created_at')
    list_filter    = ('status', 'service__category', 'created_at')
    search_fields  = ('user__username', 'user__email', 'project_name', 'service__name')
    readonly_fields = ('created_at', 'updated_at')
    list_editable  = ('status',)

    fieldsets = (
        ('Client & Service', {
            'fields': ('user', 'service', 'status')
        }),
        ('Project Details', {
            'fields': ('project_name', 'project_description', 'budget_range', 'deadline')
        }),
        ('Internal Notes', {
            'fields': ('admin_notes',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
