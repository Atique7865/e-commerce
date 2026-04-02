"""
services/admin.py
Admin panel configuration for Services.
"""
from django.contrib import admin
from .models import Service, ServiceFeature


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 3


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display   = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter    = ('category', 'is_active')
    search_fields  = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines        = [ServiceFeatureInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'icon_class', 'is_active')
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
