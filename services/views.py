"""
services/views.py
Public listing and detail views for TalentHeart services.
"""
from django.shortcuts import render, get_object_or_404
from .models import Service


def service_list(request):
    """Show all active services, optionally filtered by category."""
    category = request.GET.get('category', '')
    services = Service.objects.filter(is_active=True).prefetch_related('features')

    if category:
        services = services.filter(category=category)

    # Group by category for the template
    categories = Service.CATEGORY_CHOICES

    return render(request, 'services/list.html', {
        'services':        services,
        'categories':      categories,
        'active_category': category,
    })


def service_detail(request, slug):
    """Show full details of a single service."""
    service = get_object_or_404(Service, slug=slug, is_active=True)

    # Related services in the same category (excluding this one)
    related = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(pk=service.pk)[:3]

    return render(request, 'services/detail.html', {
        'service': service,
        'related': related,
    })
